import datetime

from invenio_db import db
from oarepo_runtime.datastreams import BaseWriter, StreamBatch
from oarepo_runtime.uow import BulkUnitOfWork

from oarepo_oaipmh_harvester.oai_batch.proxies import current_service as batch_service
from oarepo_oaipmh_harvester.oai_record.proxies import current_service as record_service
from oarepo_oaipmh_harvester.oai_run.proxies import current_service as run_service


class OAIWriter(BaseWriter):
    def __init__(self, *, identity, **kwargs) -> None:
        super().__init__()
        self._identity = identity

    def write(self, batch: StreamBatch, *args, **kwargs):
        with BulkUnitOfWork() as uow:
            self.create_oai_records(batch, uow)
            self.set_batch_status(batch, uow)
            uow.commit()

        batch_service.indexer.refresh()

        oai_run = run_service.read(self._identity, batch.context["run_id"]).data

        if batch.last:
            oai_run["batches"] = batch.seq
            run_service.update(self._identity, oai_run["id"], dict(oai_run))

        if oai_run["batches"]:
            self.set_run_status(batch, oai_run)
            db.session.expunge_all()
        return batch

    def create_oai_records(self, batch, uow):
        oai_record_ids = [
            entry.context["oai"].get("oai_record_id") for entry in batch.entries
        ]
        oai_record_ids = [x for x in oai_record_ids if x]

        oai_records = {
            x["oai_identifier"]: x
            for x in list(
                record_service.scan(
                    self._identity,
                    params={"facets": {"id": oai_record_ids}},
                )
            )
        }

        for entry in batch.entries:
            oai_id = entry.context["oai"]["identifier"]
            oai_rec = oai_records.get(oai_id)

            update = True
            if not oai_rec:
                update = False
                oai_rec = {
                    "oai_identifier": entry.context["oai"]["identifier"],
                }
                if entry.id:
                    oai_rec["local_identifier"] = entry.id

            if entry.ok:
                oai_rec["status"] = "O"
            elif entry.errors:
                oai_rec["status"] = "E"
            elif entry.filtered:
                oai_rec["status"] = "S"
            if entry.errors:
                oai_rec["errors"] = [err.json for err in entry.errors]
            elif "errors" in oai_rec:
                del oai_rec["errors"]
            oai_rec["datestamp"] = entry.context["oai"]["datestamp"]

            # add entry only on errors, no need to add it on normal records as the entry has been stored
            # and pid & version are in the context
            if entry.errors:
                oai_rec["entry"] = entry.entry

            oai_rec["context"] = entry.context
            oai_rec["batch"] = {"id": batch.context["batch_id"]}
            oai_rec["manual"] = entry.context["manual"]
            oai_rec["harvester"] = {"id": entry.context["oai_harvester_id"]}

            if update:
                record_service.update(self._identity, oai_rec["id"], oai_rec, uow=uow)
            else:
                record_service.create(self._identity, oai_rec, uow=uow)

    def set_batch_status(self, batch, uow):
        batch_id = batch.context["batch_id"]
        batch_data = batch_service.read(self._identity, batch_id).data
        status = "O"
        identifiers = []
        errors = []
        for e in batch.entries:
            if e.errors:
                status = "E"
                for err in e.errors:
                    err = err.json
                    err.pop("info", None)
                    errors.append(
                        {"oai_identifier": e.context["oai"]["identifier"], **err}
                    )
            identifiers.append(e.context["oai"]["identifier"])
        batch_data["status"] = status
        batch_data["identifiers"] = identifiers
        batch_data["finished"] = datetime.datetime.utcnow().isoformat() + "+00:00"
        if errors:
            batch_data["errors"] = errors
        batch_service.update(self._identity, batch_id, batch_data, uow=uow)

    def set_run_status(self, batch, oai_run):
        batches = list(
            batch_service.scan(
                self._identity,
                params={
                    "facets": {
                        "status": ["O", "W", "E", "I"],
                        "run_id": [batch.context["run_id"]],
                    }
                },
            )
        )
        if len(batches) == oai_run["batches"]:
            # if so, finish the run. Note: due to lack of transactions,
            # run might remain unfinished in rare cases.
            # Cleaning task should be employed.
            status = "O"
            for b in batches:
                if status == "O":
                    if b["status"] == "W":
                        status = "W"
                    elif b["status"] == "I":
                        status = "I"
                if b["status"] == "E":
                    status = "E"
                if b["status"] == "R":
                    status = "R"
                    break
            if status != "R":
                oai_run["status"] = status
                oai_run["finished"] = datetime.datetime.utcnow().isoformat() + "+00:00"
                oai_run["duration"] = (
                    datetime.datetime.fromisoformat(oai_run["finished"])
                    - datetime.datetime.fromisoformat(oai_run["started"])
                ).total_seconds()
                run_service.update(self._identity, oai_run["id"], oai_run)

import datetime

from oarepo_runtime.datastreams import BaseWriter, StreamBatch
from oarepo_runtime.records import select_record_for_update
from oarepo_runtime.uow import BulkUnitOfWork

from oarepo_oaipmh_harvester.oai_batch.proxies import current_service as batch_service
from oarepo_oaipmh_harvester.oai_record.proxies import (
    current_service as oai_record_service,
)
from oarepo_oaipmh_harvester.oai_run.proxies import current_service as run_service


class OAIWriter(BaseWriter):
    def __init__(self, *, identity, **kwargs) -> None:
        super().__init__()
        self._identity = identity

    def write(self, batch: StreamBatch, *args, **kwargs):
        with BulkUnitOfWork() as uow:
            self.update_oai_records(batch, uow)
            self.set_batch_status(batch, uow)
            uow.commit()

        batch_service.indexer.refresh()

        select_record_for_update(run_service.config.record_cls, batch.context["run_id"])
        oai_run = run_service.read(self._identity, batch.context["run_id"]).data

        if batch.last:
            oai_run["total_batches"] = batch.seq
        oai_run["finished_batches"] = oai_run.get("finished_batches", 0) + 1

        self.set_run_status(batch, oai_run)

        run_service.update(self._identity, oai_run["id"], dict(oai_run))

        return batch

    def update_oai_records(self, batch, uow):
        oai_record_ids = [
            entry.context["oai"].get("oai_record_id") for entry in batch.entries
        ]
        oai_record_ids = [x for x in oai_record_ids if x]
        if oai_record_ids:
            # TODO: better escaping if we change the pid format
            query = "id:({})".format(" OR ".join(f'"{x}"' for x in oai_record_ids))

            oai_records = {
                x["oai_identifier"]: x
                for x in list(
                    oai_record_service.scan(
                        self._identity,
                        params={"q": query},
                    )
                )
            }
        else:
            oai_records = {}

        for entry in batch.entries:
            oai_id = entry.context["oai"]["identifier"]
            oai_record_data = oai_records.get(oai_id)

            if entry.errors:
                self.create_oai_record_with_error(batch, entry, oai_record_data, uow)
            elif oai_record_data:
                self.remove_oai_record_with_error(oai_record_data, uow)

    def create_oai_record_with_error(self, batch, entry, oai_record_data, uow):
        update = True
        if not oai_record_data:
            update = False
            oai_record_data = {
                "oai_identifier": entry.context["oai"]["identifier"],
            }
            if entry.id:
                oai_record_data["oairecord_identifier"] = entry.id

        self.update_oai_record_metadata(batch, entry, oai_record_data)

        if update:
            oai_record = oai_record_service.update(
                self._identity, oai_record_data["id"], oai_record_data, uow=uow
            )
        else:
            oai_record = oai_record_service.create(
                self._identity, oai_record_data, uow=uow
            )
        entry.context["oai"]["local_oai_record_id"] = oai_record["id"]
        entry.context["oai"]["local_oai_record_ui_path"] = oai_record["links"][
            "self_html"
        ]

    def remove_oai_record_with_error(self, oai_record_data, uow):
        oai_record_service.delete(self._identity, oai_record_data["id"], uow=uow)

    def update_oai_record_metadata(self, batch, entry, oai_record_data):
        if entry.errors:
            oai_record_data["errors"] = [err.json for err in entry.errors]
        oai_record_data["datestamp"] = entry.context["oai"]["datestamp"]
        oai_record_data["entry"] = entry.entry
        oai_record_data["context"] = entry.context
        oai_record_data["batch"] = {"id": batch.context["batch_id"]}
        oai_record_data["run"] = {"id": batch.context["run_id"]}
        oai_record_data["manual"] = entry.context["manual"]
        oai_record_data["harvester"] = {"id": entry.context["oai_harvester_id"]}
        title = self._get_entry_title(entry)
        if title:
            oai_record_data["title"] = title

    @staticmethod
    def _get_entry_title(entry):
        if entry.entry.get("title"):
            return str(entry.entry["title"])
        if entry.entry.get("metadata", {}).get("title"):
            return str(entry.entry["metadata"]["title"])

    def set_batch_status(self, batch, uow):
        batch_id = batch.context["batch_id"]
        batch_data = batch_service.read(self._identity, batch_id).data
        status = "O"
        records = []
        for e in batch.entries:
            if e.filtered:
                continue

            rec = {"oai_identifier": e.context["oai"]["identifier"]}
            title = self._get_entry_title(e)
            if title:
                rec["title"] = title

            records.append(rec)
            if e.id:
                rec["local_record_identifier"] = e.id
                rec["url"] = e.entry["links"]["self_html"]
            if e.errors:
                status = "E"

                errors = []
                rec["local_error_identifier"] = e.context["oai"]["local_oai_record_id"]
                rec["url"] = e.context["oai"]["local_oai_record_ui_path"]
                rec["errors"] = errors

                for err in e.errors:
                    err = err.json
                    err.pop("info", None)
                    errors.append(err)

        batch_data["status"] = status
        batch_data["records"] = records
        batch_data["finished"] = datetime.datetime.utcnow().isoformat() + "+00:00"
        batch_service.update(self._identity, batch_id, batch_data, uow=uow)

    @staticmethod
    def set_run_status(batch, oai_run):
        if oai_run["finished_batches"] == oai_run["total_batches"]:
            status = "O"
            if oai_run.get("errors"):
                status = "E"

            oai_run["status"] = status
            oai_run["finished"] = datetime.datetime.utcnow().isoformat() + "+00:00"
            oai_run["duration"] = (
                datetime.datetime.fromisoformat(oai_run["finished"])
                - datetime.datetime.fromisoformat(oai_run["started"])
            ).total_seconds()

        oai_run["errors"] = (
            oai_run.get("errors", 0)
            + len(batch.errors)
            + sum(len(entry.errors) for entry in batch.entries)
        )

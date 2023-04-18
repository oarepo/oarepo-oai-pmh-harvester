import datetime
import traceback

from invenio_db import db
from oarepo_runtime.datastreams.config import DATASTREAMS_WRITERS, get_instance
from oarepo_runtime.datastreams.errors import WriterError
from oarepo_runtime.datastreams.writers import BatchWriter, StreamBatch

from oarepo_oaipmh_harvester.oai_batch.proxies import current_service as batch_service
from oarepo_oaipmh_harvester.oai_record.proxies import current_service as record_service
from oarepo_oaipmh_harvester.oai_run.proxies import current_service as run_service
from oarepo_oaipmh_harvester.proxies import current_harvester
from oarepo_oaipmh_harvester.uow import BulkUnitOfWork


class OAIWriter(BatchWriter):
    def __init__(self, *, identity, **kwargs) -> None:
        super().__init__()
        self.params = kwargs
        writer_params = {
            "identity": identity,
            **self.params,
            **current_harvester.get_writer_config(self.params["target_writer"]),
        }
        writer_params.pop("target_writer")
        self.writer = get_instance(DATASTREAMS_WRITERS, "writer", writer_params)
        self._identity = identity

    def write_batch(self, batch: StreamBatch, *args, **kwargs):
        with BulkUnitOfWork() as uow:
            with db.session.begin_nested():
                if batch.entries:
                    self.read_oai_records(batch)
                    batch = self.write_entries(batch, args, kwargs, uow)
                    self.create_oai_records(batch, uow)

                self.set_batch_status(batch, uow)

                oai_run = run_service.read(self._identity, batch.context["run_id"]).data

                # if it is the last batch, update oai_run with the number of batches
                if batch.last:
                    oai_run["batches"] = batch.seq
                    run_service.update(self._identity, oai_run["id"], dict(oai_run))

            uow.commit()
        db.session.expunge_all()

        # if the run already has number of batches, we might have been the latest batch.
        # check if all batches have already finished and if so, set the run as finished
        if oai_run["batches"]:
            self.set_run_status(batch, oai_run)
        db.session.expunge_all()

        return batch

    def set_run_status(self, batch, oai_run):
        batches = list(
            batch_service.scan(
                self._identity,
                params={
                    "status": ["O", "W", "E", "I"],
                    "run_id": [batch.context["run_id"]],
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
                oai_run["finished"] = datetime.datetime.utcnow().isoformat()
                oai_run["duration"] = (
                    datetime.datetime.fromisoformat(oai_run["finished"])
                    - datetime.datetime.fromisoformat(oai_run["started"])
                ).total_seconds
                run_service.update(self._identity, oai_run["id"], oai_run)

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
                    errors.append(
                        {"oai_identifier": e.context["oai"]["identifier"], "error": err}
                    )
            identifiers.append(e.context["oai"]["identifier"])
        batch_data["status"] = status
        batch_data["identifiers"] = identifiers
        batch_data["finished"] = datetime.datetime.utcnow().isoformat()
        if errors:
            batch_data["errors"] = errors
        batch_service.update(self._identity, batch_id, batch_data, uow=uow)

    def read_oai_records(self, batch):
        oai_records = {
            x["oai_identifier"]: x
            for x in list(
                record_service.scan(
                    self._identity,
                    params={
                        "facets": {
                            "oai_identifier": [
                                e.context["oai"]["identifier"] for e in batch.entries
                            ]
                        }
                    },
                )
            )
        }
        for e in batch.entries:
            oai_rec = oai_records.get(e.context["oai"]["identifier"])
            if oai_rec and oai_rec.get("local_identifier"):
                e.entry["id"] = oai_rec["local_identifier"]
                if oai_rec["datestamp"] == e.context["oai"]["datestamp"]:
                    # do not save the item as it has the same datestamp
                    e.filtered = True

    def create_oai_records(self, batch, uow):
        oai_records = {
            x["oai_identifier"]: x
            for x in list(
                record_service.scan(
                    self._identity,
                    params={
                        "facets": {
                            "oai_identifier": [
                                e.context["oai"]["identifier"] for e in batch.entries
                            ]
                        }
                    },
                )
            )
        }
        for e in batch.entries:
            oai_rec = oai_records.get(e.context["oai"]["identifier"])
            if oai_rec:
                update = True
                if oai_rec["datestamp"] == e.context["oai"]["datestamp"]:
                    # do not update the oairec if the datestamp has not changed
                    continue
            else:
                update = False
                oai_rec = {
                    "oai_identifier": e.context["oai"]["identifier"],
                }
                local_identifier = e.entry.get("id")
                if local_identifier:
                    oai_rec["local_identifier"] = local_identifier
            if e.ok:
                oai_rec["status"] = "O"
            elif e.errors:
                oai_rec["status"] = "E"
            elif e.filtered:
                oai_rec["status"] = "S"
            # TODO: warnings
            if e.errors:
                oai_rec["errors"] = [str(x) for x in e.errors]
            elif "errors" in oai_rec:
                del oai_rec["errors"]
            oai_rec["datestamp"] = e.context["oai"]["datestamp"]
            oai_rec["entry"] = e.entry
            oai_rec["context"] = e.context
            oai_rec["batch"] = {"id": batch.context["batch_id"]}
            if update:
                record_service.update(self._identity, oai_rec["id"], oai_rec, uow=uow)
            else:
                record_service.create(self._identity, oai_rec, uow=uow)

    def write_entries(self, batch: StreamBatch, args, kwargs, uow):
        # TODO: write only if the entry has been modified
        if hasattr(self.writer, "write_batch"):
            # split the batch do deleted and normal items
            persisted_entries = []
            skipped_entries = []
            deleted_entries = []
            for e in batch.entries:
                if not e.ok:
                    skipped_entries.append(e)
                elif e.context["oai"]["deleted"]:
                    deleted_entries.append(e)
                else:
                    persisted_entries.append(e)
            if persisted_entries:
                persisted_entries = self.writer.write_batch(
                    batch.copy(entries=persisted_entries), uow=uow
                ).entries
            if deleted_entries:
                for entry in deleted_entries:
                    try:
                        self.delete_entry(entry, uow)
                    except WriterError as e:
                        stack = "\n".join(traceback.format_stack())
                        entry.errors.append(f"Writer {self.writer} error: {e}: {stack}")
                    except Exception as e:
                        stack = "\n".join(traceback.format_stack())
                        entry.errors.append(
                            f"Writer {self.writer} unhandled error: {e}: {stack}"
                        )
            batch.entries = persisted_entries + skipped_entries + deleted_entries
            return batch
        else:
            for entry in batch.entries:
                if entry.ok:
                    try:
                        if entry.context["oai"]["deleted"]:
                            self.delete_entry(entry, uow)
                        else:
                            self.writer.write(entry, uow=uow)
                    except WriterError as e:
                        stack = traceback.format_exc()
                        entry.errors.append(f"Writer {self.writer} error: {e}: {stack}")
                    except Exception as e:
                        stack = traceback.format_exc()
                        entry.errors.append(
                            f"Writer {self.writer} unhandled error: {e}: {stack}"
                        )
        return batch

    def delete_entry(self, entry, uow):
        oai_record = list(
            record_service.scan(
                self._identity,
                params={"facets": {"oai_identifier": [entry.context["oai"]["identifier"]]}},
            )
        )
        if oai_record and "local_identifier" in oai_record[0]:
            entry.entry["id"] = oai_record[0]["local_identifier"]
            self.writer.delete(entry, uow=uow)

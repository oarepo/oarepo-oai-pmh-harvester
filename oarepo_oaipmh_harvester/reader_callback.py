import datetime

from oarepo_runtime.datastreams import StreamBatch
from oarepo_runtime.records import select_record_for_update

from oarepo_oaipmh_harvester.oai_batch.proxies import current_service as batch_service
from oarepo_oaipmh_harvester.oai_run.proxies import current_service as run_service


def reader_callback(batch: StreamBatch, *, identity, oai_run, manual, oai_harvester):
    batch_el = batch_service.create(
        identity,
        {
            "run": {"id": oai_run},
            "harvester": {"id": oai_harvester},
            "status": "R",
            "records": [
                {"oai_identifier": x.context["oai"]["identifier"]}
                for x in batch.entries
            ],
            "started": datetime.datetime.utcnow().isoformat() + "+00:00",
            "manual": manual,
            "sequence": batch.seq,
        },
    )
    batch.context["batch_id"] = batch_el["id"]
    for e in batch.entries:
        e.context["oai_batch"] = batch_el["id"]
        e.context["manual"] = manual

    # select for update till the end of transaction
    select_record_for_update(run_service.config.record_cls, batch.context["run_id"])
    oai_run = run_service.read(identity, batch.context["run_id"]).data
    oai_run["created_batches"] = oai_run.get("created_batches", 0) + 1
    run_service.update(identity, batch.context["run_id"], oai_run)

    return batch

import datetime
from typing import Dict, Union

import celery
from invenio_access.permissions import system_identity
from oarepo_runtime.datastreams import StreamEntry
from oarepo_runtime.tasks.datastreams import AsyncDataStream

from oarepo_oaipmh_harvester.oai_harvester.proxies import (
    current_service as harvester_service,
)
from oarepo_oaipmh_harvester.oai_harvester.records.api import OaiHarvesterRecord
from oarepo_oaipmh_harvester.oai_run.proxies import current_service as run_service
from oarepo_oaipmh_harvester.proxies import current_harvester


def harvest(
    harvester_or_code: Union[str, OaiHarvesterRecord, Dict],
    all_records=False,
    on_background=False,
    identifiers=None,
    progress_callback=None,
):
    if isinstance(harvester_or_code, str):
        harvesters = list(
            harvester_service.scan(
                system_identity,
                params={"facets": {"code": [harvester_or_code]}},
            )
        )
        harvester = harvesters[0]
    else:
        harvester = harvester_or_code
    harvester = dict(harvester)

    harvester.pop("links", None)
    harvester.pop("created", None)
    harvester.pop("updated", None)
    harvester.pop("revision_id", None)

    run = run_service.create(
        system_identity,
        {
            "harvester": harvester,
            "status": "R",
            "batches": 0,
            "started": datetime.datetime.utcnow().isoformat(),
        },
    )
    run_id = run["id"]

    reader_config = current_harvester.get_parser_config(harvester["loader"])
    reader_config = {
        "source": harvester["baseurl"],
        **reader_config,
        "all_records": all_records,
        "identifiers": identifiers,
        "config": dict(harvester),
        "oai_run": run_id,
    }

    transformers_config = [
        {
            **current_harvester.get_transformer_config("oai_batch"),
            "config": dict(harvester),
            "oai_run": run_id,
        }
    ]
    transformers_config.extend(
        {
            **current_harvester.get_transformer_config(x),
            "config": dict(harvester),
        }
        for x in harvester["transformers"]
    )

    writer_config = {
        "writer": "oai",
        "target_writer": harvester["writer"],
    }

    def progress(read, run_id=None, **kwargs):
        if progress_callback and (read % 100) == 0:
            progress_callback(read)

    datastream = AsyncDataStream(
        readers=[reader_config],
        writers=[writer_config],
        transformers=transformers_config,
        success_callback=harvester_success.signature(),
        error_callback=harvester_error.signature(),
        progress_callback=progress,
        batch_size=harvester["batch_size"],
        in_process=not on_background,
        extra_parameters={"run": run_id},
        identity=system_identity,
    )

    datastream.process()


@celery.shared_task
def harvester_success(*args, entry: StreamEntry = None, **kwargs):
    pass
    # print("success", entry)


@celery.shared_task
def harvester_error(*args, entry: StreamEntry = None, **kwargs):
    if entry:
        print("Error in oai identifier", entry.context.get("oai", {}).get("identifier"))
        for e in entry.errors:
            print(e)
        print()
    else:
        print("Unexpected error", *args, **kwargs)

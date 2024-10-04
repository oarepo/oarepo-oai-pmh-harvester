import datetime
from functools import partial
from typing import Dict, Union

from invenio_access.permissions import system_identity
from invenio_search import current_search_client
from invenio_search.utils import build_alias_name
from oarepo_runtime.datastreams import SynchronousDataStream
from oarepo_runtime.datastreams.asynchronous import AsynchronousDataStream
from oarepo_runtime.datastreams.datastreams import Signature
from oarepo_runtime.datastreams.fixtures import fixtures_asynchronous_callback
from oarepo_runtime.datastreams.types import StatsKeepingDataStreamCallback

from oarepo_oaipmh_harvester.oai_harvester.proxies import (
    current_service as harvester_service,
)
from oarepo_oaipmh_harvester.oai_harvester.records.api import OaiHarvesterRecord
from oarepo_oaipmh_harvester.oai_record.records.api import OaiRecord
from oarepo_oaipmh_harvester.oai_run.proxies import current_service as run_service
from oarepo_oaipmh_harvester.proxies import current_harvester
from oarepo_oaipmh_harvester.reader_callback import reader_callback


def _get_max_datestamp_query(harvester):
    max_datestamp_query = {
        "query": {
            "bool": {
                "filter": [
                    {"term": {"harvester.id": harvester}},
                    {"term": {"manual": False}},
                ]
            }
        },
        "size": 0,
        "aggs": {"max_datestamp": {"max": {"field": "datestamp"}}},
    }
    return max_datestamp_query


def _get_latest_oai_datestamp(harvester_id):
    index = build_alias_name(OaiRecord.index.search_alias)
    result = current_search_client.search(
        index=index,
        body=_get_max_datestamp_query(harvester_id),
    )
    result = result["aggregations"]["max_datestamp"]["value"]
    ret = datetime.datetime.utcfromtimestamp(result / 1000).date() if result else None
    return ret


def harvest(
    harvester_or_code: Union[str, OaiHarvesterRecord, Dict],
    all_records=False,
    on_background=False,
    identifiers=None,
    callback=None,
    on_run_created=None,
    title=None,
    overwrite_all_records=False,
):
    if isinstance(harvester_or_code, str):
        harvesters = list(
            harvester_service.scan(
                system_identity,
                params={"facets": {"code": [harvester_or_code]}},
            )
        )
        if hasattr(harvesters[0], "data"):
            harvester = harvesters[0].data
        else:
            harvester = harvesters[0]
    else:
        harvester = harvester_or_code
    harvester = dict(harvester)

    harvester.pop("links", None)
    harvester.pop("created", None)
    harvester.pop("updated", None)
    harvester.pop("revision_id", None)

    run_manual = True if identifiers else False
    run_metadata = {
        "harvester": {"id": harvester["id"]},
        "errors": 0,
        "status": "R",
        "created_batches": 0,
        "total_batches": 0,
        "finished_batches": 0,
        "started": datetime.datetime.utcnow().isoformat() + "+00:00",
        "manual": run_manual,
    }
    if title:
        run_metadata["title"] = title

    run = run_service.create(
        system_identity,
        run_metadata,
    )
    run_id = run["id"]
    if on_run_created:
        on_run_created(run_id)

    start_from = _get_latest_oai_datestamp(harvester["id"]) if not run_manual else None

    reader_signature: Signature = current_harvester.get_parser_signature(
        harvester["loader"],
        source=harvester["baseurl"],
        all_records=all_records,
        identifiers=identifiers,
        oai_config=dict(harvester),
        oai_run=run_id,
        start_from=start_from,
        oai_harvester_id=harvester["id"],
        manual=run_manual,
    )

    transformers_signatures = [
        current_harvester.get_transformer_signature(
            transformer,
            oai_config=dict(harvester),
            oai_run=run_id,
            oai_harvester_id=harvester["id"],
            manual=run_manual,
        )
        for transformer in harvester["transformers"]
    ]

    writers_signatures = [
        current_harvester.get_writer_signature(writer)
        for writer in harvester["writers"]
    ]

    t: Signature
    for t in transformers_signatures:
        if t.name == "oai_record_lookup":
            break
    else:
        t = current_harvester.get_transformer_signature(
            "oai_record_lookup",
            oai_config=dict(harvester),
            oai_run=run_id,
            oai_harvester_id=harvester["id"],
            manual=run_manual,
            overwrite_all_records=overwrite_all_records,
        )
        transformers_signatures.append(t)

    for writer_signature in writers_signatures:
        if writer_signature.name == "service" or writer_signature.name == "published_service":
            t.kwargs["harvested_record_service"] = writer_signature.kwargs["service"]

    writers_config = [
        *writers_signatures,
        current_harvester.get_writer_signature(
            "oai",
            oai_config=dict(harvester),
            oai_run=run_id,
            oai_harvester_id=harvester["id"],
            manual=run_manual,
        ),
    ]

    if not on_background:
        datastream_impl = partial(
            SynchronousDataStream,
            callback=callback or StatsKeepingDataStreamCallback(log_error_entry=True),
        )
    else:
        datastream_impl = partial(
            AsynchronousDataStream,
            on_background=True,
            callback=callback or fixtures_asynchronous_callback.s(),
        )

    datastream = datastream_impl(
        readers=[reader_signature],
        writers=writers_config,
        transformers=transformers_signatures,
        batch_size=harvester.get("batch_size", 10),
        reader_callback=partial(
            reader_callback,
            identity=system_identity,
            oai_run=run_id,
            manual=run_manual,
            oai_harvester=harvester["id"],
        ),
    )

    datastream.process(identity=system_identity, context={"run_id": run_id})

    return run_id

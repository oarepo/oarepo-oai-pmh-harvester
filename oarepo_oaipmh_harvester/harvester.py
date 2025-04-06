import datetime
from functools import partial
from typing import Dict, Union

from invenio_access.permissions import system_identity
from invenio_db import db
from oarepo_runtime.datastreams import SynchronousDataStream
from oarepo_runtime.datastreams.asynchronous import AsynchronousDataStream
from oarepo_runtime.datastreams.datastreams import Signature
from oarepo_runtime.datastreams.fixtures import fixtures_asynchronous_callback
from oarepo_runtime.datastreams.types import StatsKeepingDataStreamCallback
from sqlalchemy import func

from oarepo_oaipmh_harvester.models import OAIHarvestedRecord, OAIHarvesterRun
from oarepo_oaipmh_harvester.oai_harvester.proxies import (
    current_service as harvester_service,
)
from oarepo_oaipmh_harvester.oai_harvester.records.api import OaiHarvesterRecord
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
    max_datestamp = (
        db.session.query(func.max(OAIHarvestedRecord.datestamp))
        .join(OAIHarvesterRun)
        .filter(OAIHarvesterRun.harvester_id == harvester_id)
        .filter(OAIHarvesterRun.manual.is_(False))
        .scalar()
    )
    return max_datestamp


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

    print("Will harvest using harvester", harvester)

    run_manual = True if identifiers else False

    run = OAIHarvesterRun(
        harvester_id=harvester["id"],
        harvester_config=dict(harvester),
        start_time=datetime.datetime.utcnow(),
        status="running",
        manual=run_manual,
        title=title,
    )
    db.session.add(run)
    db.session.commit()

    str_run_id = str(run.id)

    if on_run_created:
        on_run_created(str_run_id)

    start_from = _get_latest_oai_datestamp(harvester["id"]) if not run_manual else None

    reader_signature: Signature = current_harvester.get_parser_signature(
        harvester["loader"],
        source=harvester["baseurl"],
        all_records=all_records,
        identifiers=identifiers,
        oai_config=dict(harvester),
        oai_run=str_run_id,
        start_from=start_from,
        oai_harvester_id=harvester["id"],
        manual=run_manual,
    )

    transformers_signatures = [
        current_harvester.get_transformer_signature(
            transformer,
            oai_config=dict(harvester),
            oai_run=str_run_id,
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
            oai_run=str_run_id,
            oai_harvester_id=harvester["id"],
            manual=run_manual,
            overwrite_all_records=overwrite_all_records,
        )
        transformers_signatures.append(t)

    for writer_signature in writers_signatures:
        if (
            writer_signature.name == "service"
            or writer_signature.name == "published_service"
        ):
            t.kwargs["harvested_record_service"] = writer_signature.kwargs["service"]

    writers_config = [
        *writers_signatures,
        current_harvester.get_writer_signature(
            "oai",
            oai_config=dict(harvester),
            oai_run=str_run_id,
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
            oai_run=str_run_id,
            manual=run_manual,
            oai_harvester=harvester["id"],
        ),
    )

    datastream.process(identity=system_identity, context={"run_id": str_run_id})

    return run.id

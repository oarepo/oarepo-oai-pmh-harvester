import datetime
from pathlib import Path

from invenio_access.permissions import system_identity
from invenio_records_resources.tasks import manage_indexer_queues

from oarepo_oaipmh_harvester.cli import _add_harvester
from oarepo_oaipmh_harvester.models import OAIHarvestedRecord, OAIHarvesterRun
from oarepo_oaipmh_harvester.proxies import (
    current_oai_record_service,
)


def test_oai_record_indexing(app, db, search_clear, default_community, mappings):

    harvester_metadata = {
        "code": "test",
        "baseurl": (Path(__file__).parent / "harvest_data.json").as_uri(),
        "metadataprefix": "test",
        "comment": "comment",
        "name": "Test harvester",
        "setspecs": "test",
        "loader": "file",
        "transformers": [
            "error_transformer",
            "set_community{community=default}",
        ],
        "writers": [
            "service{service=test_model,update=true}",
            "publish{service=test_model,direct_call=true}",
        ],
        "batch_size": 6,
    }
    harvester = _add_harvester(harvester_metadata)

    run = OAIHarvesterRun(
        harvester_id=harvester["id"],
        status="running",
        finished_records=100,
        failed_records=10,
        ok_records=90,
        start_time=datetime.datetime.utcnow(),
        last_update_time=datetime.datetime.utcnow(),
        manual=False,
    )
    db.session.add(run)
    db.session.commit()

    record = OAIHarvestedRecord(
        run_id=run.id,
        oai_identifier="oai:test:1",
        datestamp=datetime.datetime.utcnow(),
        deleted=False,
        has_errors=False,
        has_warnings=False,
        original_data=dict(),
        transformed_data=dict(),
    )
    db.session.add(record)
    db.session.commit()

    current_oai_record_service.indexer.bulk_index([record.oai_identifier])
    manage_indexer_queues()
    current_oai_record_service.indexer.refresh()

    hits = list(
        current_oai_record_service.search(
            system_identity, facets=dict(harvester_id=[harvester["id"]])
        )
    )
    print(hits)
    assert len(hits) == 1
    assert hits[0]["id"] == str(record.oai_identifier)

    hits = list(
        current_oai_record_service.search(
            system_identity, facets=dict(run_id=[str(run.id)])
        )
    )
    assert len(hits) == 1
    assert hits[0]["id"] == str(record.oai_identifier)

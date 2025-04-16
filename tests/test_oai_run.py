import datetime
from pathlib import Path

from invenio_access.permissions import system_identity
from invenio_records_resources.tasks import manage_indexer_queues

from oarepo_oaipmh_harvester.cli import _add_harvester
from oarepo_oaipmh_harvester.models import OAIHarvesterRun
from oarepo_oaipmh_harvester.proxies import current_oai_run_service


def test_oai_run_indexing(app, db, search_clear, default_community, mappings):

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

    harvester_metadata["code"] = "test2"
    harvester2 = _add_harvester(harvester_metadata)

    run2 = OAIHarvesterRun(
        harvester_id=harvester2["id"],
        status="failed",
        manual=True,
        start_time=datetime.datetime.utcnow(),
    )
    db.session.add(run2)
    db.session.commit()

    current_oai_run_service.indexer.bulk_index([run.id, run2.id])
    manage_indexer_queues()
    current_oai_run_service.indexer.refresh()

    hits = list(
        current_oai_run_service.search(
            system_identity, facets=dict(harvester=[harvester["id"]])
        )
    )
    assert len(hits) == 1
    assert hits[0]["id"] == str(run.id)

    hits = list(
        current_oai_run_service.search(system_identity, facets=dict(manual=[True]))
    )
    assert len(hits) == 1
    assert hits[0]["id"] == str(run2.id)

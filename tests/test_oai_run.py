import datetime

from invenio_access.permissions import system_identity
from invenio_records_resources.tasks import manage_indexer_queues

from oarepo_oaipmh_harvester.models import OAIHarvesterRun
from oarepo_oaipmh_harvester.proxies import current_oai_run_service


def test_oai_run_indexing(app, db, search_clear, default_community, mappings):
    run = OAIHarvesterRun(
        harvester_id="test",
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

    run2 = OAIHarvesterRun(
        harvester_id="test1",
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
        current_oai_run_service.search(system_identity, facets=dict(harvester=["test"]))
    )
    assert len(hits) == 1
    assert hits[0]["id"] == str(run.id)

    hits = list(
        current_oai_run_service.search(system_identity, facets=dict(manual=[True]))
    )
    assert len(hits) == 1
    assert hits[0]["id"] == str(run2.id)

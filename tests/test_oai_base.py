import pytest

from invenio_oarepo_oai_pmh_harvester.models import OAISync
from invenio_oarepo_oai_pmh_harvester.oai_base import OAIDBBase


def test_init(app, test_db, migrate_provider):
    base = OAIDBBase(migrate_provider)
    assert base.provider == migrate_provider


def test_run(app, test_db, migrate_provider):
    base = OAIDBBase(migrate_provider)
    base.run()
    sync = OAISync.query.get(1)
    assert sync.status == "ok"
    assert sync.sync_end is not None
    assert sync.sync_start is not None


def test_run_failed(app, test_db, migrate_provider):
    class OAIDBBaseFailed(OAIDBBase):
        def synchronize(self):
            assert False, "Testing exception handling"

    base = OAIDBBaseFailed(migrate_provider)
    with pytest.raises(AssertionError):
        base.run()
    sync = OAISync.query.get(1)
    assert sync.status == "failed"
    assert sync.sync_end is not None
    assert sync.sync_start is not None
    assert len(sync.logs) > 0

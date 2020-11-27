from typing import Callable
from unittest import mock

from invenio_records import Record

from oarepo_oai_pmh_harvester.models import OAISync, OAIRecord
from oarepo_oai_pmh_harvester.provider import OAIProvider
from oarepo_oai_pmh_harvester.proxies import current_oai_client
from oarepo_oai_pmh_harvester.synchronization import OAISynchronizer
from tests.helpers import mock_harvest


class TestExt:
    def test_OArepoOAIClientState(self, load_entry_points, app, db):
        providers = current_oai_client.providers
        assert isinstance(providers, dict)
        keys = list(providers.keys())
        assert isinstance(providers[keys[0]], OAIProvider)
        synchronizers = providers[keys[0]].synchronizers
        assert isinstance(synchronizers, dict)
        assert isinstance(list(synchronizers.values())[0], OAISynchronizer)

    def test_run_synchronizer(self, load_entry_points, app, db):
        patch = mock.patch('sickle.app.Sickle.harvest', mock_harvest)
        patch.start()
        current_oai_client._run_synchronizer("uk", "xoai")
        patch.stop()

        oai_sync = OAISync.query.get(1)
        assert oai_sync.status == "ok"
        assert oai_sync.records_created == 1
        oai_rec = OAIRecord.query.all()[-1]
        assert oai_rec.pid == "1"
        record = Record.get_record(id_=oai_rec.id)
        assert record["title"] == "Testovací záznam"

    def test_run_provider(self, load_entry_points, app, db):
        patch = mock.patch('sickle.app.Sickle.harvest', mock_harvest)
        patch.start()
        current_oai_client._run_provider("uk")
        patch.stop()

        oai_sync = OAISync.query.get(1)
        assert oai_sync.status == "ok"
        assert oai_sync.records_created == 1
        oai_rec = OAIRecord.query.all()[-1]
        assert oai_rec.pid == "1"
        record = Record.get_record(id_=oai_rec.id)
        assert record["title"] == "Testovací záznam"

    def test_run(self, load_entry_points, app, db):
        patch = mock.patch('sickle.app.Sickle.harvest', mock_harvest)
        patch.start()
        current_oai_client.run()
        patch.stop()

        oai_sync = OAISync.query.get(1)
        assert oai_sync.status == "ok"
        assert oai_sync.records_created == 1
        oai_rec = OAIRecord.query.all()[-1]
        assert oai_rec.pid == "1"
        record = Record.get_record(id_=oai_rec.id)
        assert record["title"] == "Testovací záznam"

    def test_run_2(self, load_entry_points, app, db):
        patch = mock.patch('sickle.app.Sickle.harvest', mock_harvest)
        patch.start()
        current_oai_client.run(providers_codes=["uk"])
        patch.stop()

        oai_sync = OAISync.query.get(1)
        assert oai_sync.status == "ok"
        assert oai_sync.records_created == 1
        oai_rec = OAIRecord.query.all()[-1]
        assert oai_rec.pid == "1"
        record = Record.get_record(id_=oai_rec.id)
        assert record["title"] == "Testovací záznam"

    def test_run_3(self, load_entry_points, app, db):
        patch = mock.patch('sickle.app.Sickle.harvest', mock_harvest)
        patch.start()
        current_oai_client.run(providers_codes=["uk"], synchronizers_codes=["xoai"])
        patch.stop()

        oai_sync = OAISync.query.get(1)
        assert oai_sync.status == "ok"
        assert oai_sync.records_created == 1
        oai_rec = OAIRecord.query.all()[-1]
        assert oai_rec.pid == "1"
        record = Record.get_record(id_=oai_rec.id)
        assert record["title"] == "Testovací záznam"

    def test_load_ep(self, load_entry_points, app, db):
        res = current_oai_client.endpoint_handlers
        assert isinstance(res["uk"]["xoai"], Callable)

    def test_print_prividers(self, load_entry_points, app, db):
        for k, v in current_oai_client.providers:
            print(k, v)

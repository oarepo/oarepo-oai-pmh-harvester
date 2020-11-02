from oarepo_oai_pmh_harvester.models import OAIProvider
from oarepo_oai_pmh_harvester.proxies import current_oai_client
from oarepo_oai_pmh_harvester.synchronization import OAISynchronizer


class TestExt:
    def test_OArepoOAIClientState(self, load_entry_points, app, db):
        providers = current_oai_client.providers
        assert isinstance(providers, dict)
        keys = list(providers.keys())
        assert isinstance(providers[keys[0]], OAIProvider)
        synchronizers = providers[keys[0]]._synchronizers
        assert isinstance(synchronizers, dict)
        assert isinstance(list(synchronizers.values())[0], OAISynchronizer)

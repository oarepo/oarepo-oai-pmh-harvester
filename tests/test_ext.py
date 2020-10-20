from oarepo_oai_pmh_harvester.proxies import current_oai_client


class TestExt:
    def test_OArepoOAIClientState(self,load_entry_points, app, db):
        rules = current_oai_client.rules
        parsers = current_oai_client.parsers
        synchronizers = current_oai_client.synchronizers
        assert rules is not None
        assert parsers is not None
        assert synchronizers is not None

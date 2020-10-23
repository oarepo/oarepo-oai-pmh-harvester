from oarepo_oai_pmh_harvester.proxies import current_oai_client


class TestExt:
    def test_OArepoOAIClientState(self,load_entry_points, app, db):
        providers = current_oai_client.providers
        print(providers)


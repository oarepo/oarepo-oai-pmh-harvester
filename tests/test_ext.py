from oarepo_oai_pmh_harvester.ext import OArepoOAIClient
from oarepo_oai_pmh_harvester.proxies import current_oai_client


def test_OArepoOAIClientState(app, db):
    client = OArepoOAIClient(app)
    res = current_oai_client.rules
    res2 = current_oai_client.parsers
    print(res, res2)


def test_load_synchronizers(app, db):
    client = OArepoOAIClient(app)
    current_oai_client.load_synchronizers()

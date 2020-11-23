from oarepo_oai_pmh_harvester.decorators import endpoint_handler
from oarepo_oai_pmh_harvester.proxies import current_oai_client


def test_endpoint_handler(load_entry_points, app, db):
    @endpoint_handler("uk", "xoai")
    def handler(data):
        return "hello"

    assert current_oai_client.endpoint_handlers["uk"]["xoai"].__name__ == "handler"

from oarepo_oai_pmh_harvester.decorators import endpoint_handler, pre_processor, post_processor, \
    rule_error_handler
from oarepo_oai_pmh_harvester.proxies import current_oai_client


def test_endpoint_handler(load_entry_points, app, db):
    @endpoint_handler("uk", "xoai")
    def handler(data):
        return "hello"

    assert current_oai_client.endpoint_handlers["uk"]["xoai"].__name__ == "handler"


def test_endpoint_handler_2(load_entry_points, app, db):
    @endpoint_handler(provider_parser_list=[{"provider": "uk", "parser": "xoai"}])
    def handler(data):
        return "hello"

    assert current_oai_client.endpoint_handlers["uk"]["xoai"].__name__ == "handler"


def test_error_handler(load_entry_points, app, db):
    @rule_error_handler("uk", "xoai")
    def handler(data):
        return "hello"

    assert current_oai_client.error_handlers["uk"]["xoai"].__name__ == "handler"


def test_pre_processor(load_entry_points, app, db):
    if current_oai_client._pre_processors:
        print(current_oai_client._pre_processors)
        current_oai_client._pre_processors = None

    @pre_processor("uk", "xoai")
    def handler(data):
        print("hello")
        return data

    assert current_oai_client.pre_processors["uk"]["xoai"][0].__name__ == "handler"


def test_pre_processor_2(load_entry_points, app, db):
    if current_oai_client._pre_processors:
        print(current_oai_client._pre_processors)
        current_oai_client._pre_processors = None

    @pre_processor(provider_parser_list=[{"provider": "uk", "parser": "xoai"}])
    def handler(data):
        print("hello")
        return data

    assert current_oai_client.pre_processors["uk"]["xoai"][0].__name__ == "handler"


def test_post_processor(load_entry_points, app, db):
    if current_oai_client._post_processors:
        print(current_oai_client._post_processors)
        current_oai_client._post_processors = None

    @post_processor("uk", "xoai")
    def handler(data):
        print("hello")
        return data

    assert current_oai_client.post_processors["uk"]["xoai"][0].__name__ == "handler"


def test_post_processor_2(load_entry_points, app, db):
    if current_oai_client._post_processors:
        print(current_oai_client._post_processors)
        current_oai_client._post_processors = None

    @post_processor(provider_parser_list=[{"provider": "uk", "parser": "xoai"}])
    def handler(data):
        print("hello")
        return data

    assert current_oai_client.post_processors["uk"]["xoai"][0].__name__ == "handler"

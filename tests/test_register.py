from pprint import pprint

from invenio_oarepo_oai_pmh_harvester import registry
from invenio_oarepo_oai_pmh_harvester.register import Decorators


def test_parser_decorator():
    @Decorators.parser("test_name", "test_provider")
    def parse_bla():
        return "OK"

    result = registry.parsers
    pprint(result)
    assert result["test_provider"]["test_name"]() == "OK"

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


# TODO: Create example app due to entry_points

def test_get_parsers():
    registry.get_parsers()
    parsers = registry.parsers
    assert parsers["uk"]["xoai"].__name__ == "parser_refine"
    print(parsers)


def test_get_rules():
    registry.get_rules()
    rules = registry.rules
    func = rules["xoai"]["/dc/description/abstract"]["pre"]
    assert func.__name__ == "transform_uk_abstract"
    assert getattr(func, "_transform_path") == '/dc/description/abstract'
    assert getattr(func, "_transform_phase") == 'pre'
    print(rules)

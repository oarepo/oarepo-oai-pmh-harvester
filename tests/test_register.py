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


def test_pre_rule_decorator():
    @Decorators.rule("test_parser")
    @Decorators.pre_rule("/path/to/field")
    def sample_rule():
        return "OK"

    result = registry.rules
    assert result["test_parser"]["/path/to/field"]["pre"]() == "OK"


def test_post_rule_decorator():
    @Decorators.rule("test_parser")
    @Decorators.post_rule("/path/to/field")
    def sample_rule():
        return "OK"

    result = registry.rules
    assert result["test_parser"]["/path/to/field"]["post"]() == "OK"


def test_array_value():
    results = [[]]

    @Decorators.array_value
    def return_array_1(**kwargs):
        return ["bla"]


    @Decorators.array_value
    def return_array_2(**kwargs):
        return "spam"

    return_array_1(results=results)
    return_array_2(results=results)
    assert results == [["bla", "spam"]]
    print(results)






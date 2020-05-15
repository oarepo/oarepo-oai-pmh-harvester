from example.rules.utils import get_ref
from invenio_oarepo_oai_pmh_harvester.register import Decorators


@Decorators.rule("xoai")
@Decorators.pre_rule("/dc/contributor")
def transform_contributor(paths, el, results, phase, **kwargs):
    contributors = []
    results[-1]["contributor"] = contributors
    return contributors


@Decorators.rule("xoai")
@Decorators.pre_rule("advisor")
@Decorators.array_value
def transform_advisor(el=None, results=None, **kwargs):
    value = el["value"]
    assert len(value) == 1
    return {
        "name": value[0][0],
        "role": get_ref("advisor", "contributor-type")
    }


@Decorators.rule("xoai")
@Decorators.pre_rule("referee")
@Decorators.array_value
def transform_referee(el=None, results=None, **kwargs):
    value = el["value"]
    assert len(value) == 1
    return {
        "name": value[0][0],
        "role": get_ref("referee", "contributor-type")
    }

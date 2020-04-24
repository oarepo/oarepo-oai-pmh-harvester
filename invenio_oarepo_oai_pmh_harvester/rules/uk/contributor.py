from invenio_oarepo_oai_pmh_harvester.rules.utils import get_ref
from invenio_oarepo_oai_pmh_harvester.rules_ import pre_rule, array_value


@pre_rule("/dc/contributor")
def transform_contributor(paths, el, results, phase, **kwargs):
    contributors = []
    results[-1]["contributor"] = contributors
    return contributors


@pre_rule("advisor")
@array_value
def transform_advisor(el=None, results=None, **kwargs):
    value = el["value"]
    assert len(value) == 1
    return {
        "name": value[0],
        "role": get_ref("advisor", "contributor-type")
    }


@pre_rule("referee")
@array_value
def transform_referee(el=None, results=None, **kwargs):
    value = el["value"]
    assert len(value) == 1
    return {
        "name": value[0],
        "role": get_ref("referee", "contributor-type")
    }

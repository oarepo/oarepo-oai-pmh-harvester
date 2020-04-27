from invenio_oarepo_oai_pmh_harvester.register import Decorators
from invenio_oarepo_oai_pmh_harvester.rules.utils import get_iso_lang_code


@Decorators.rule('xoai')
@Decorators.pre_rule("/dc/title")
def transform_title(paths, el, results, phase, **kwargs):
    title = []
    results[-1]["title"] = title
    return title


@Decorators.rule('xoai')
@Decorators.pre_rule("/dc/title/cs_CZ")
@Decorators.array_value
def transform_title_cz(paths, el, results, phase, **kwargs):
    value = el["value"]
    assert len(value) == 1
    return {
        "name": value[0],
        "lang": "cze"
    }


@Decorators.rule('xoai')
@Decorators.pre_rule("/dc/title/translated")
@Decorators.array_value
def transform_title_translated(paths, el, results, phase, **kwargs):
    result = []
    for k, v in el.items():
        value_array = v[0]["value"]
        assert len(value_array) == 1
        result.append(
            {
                "value": value_array[0],
                "lang": get_iso_lang_code(k[:2])
            }
        )
    return result

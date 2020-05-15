from example.rules.utils import get_iso_lang_code
from invenio_oarepo_oai_pmh_harvester.register import Decorators
from invenio_oarepo_oai_pmh_harvester.transformer import OAITransformer


@Decorators.rule('xoai')
@Decorators.pre_rule("/dc/title")
def transform_title(paths, el, results, phase, **kwargs):
    title = []
    for k, v in el.items():
        if k == "translated":
            title.extend(transform_title_translated(v))
        else:
            title.append(
                {
                    "value": v[0]["value"][0],
                    "lang": get_iso_lang_code(k[:2])
                }
            )
    results[-1]["title"] = title
    return OAITransformer.PROCESSED


def transform_title_translated(el):
    translated_titles = []
    for k, v in el[0].items():
        value_array = v[0]["value"]
        assert len(value_array) == 1
        translated_titles.append(
            {
                "value": value_array[0],
                "lang": get_iso_lang_code(k[:2])
            }
        )
    return translated_titles

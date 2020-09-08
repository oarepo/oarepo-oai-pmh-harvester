from example.rules.utils import get_iso_lang_code
from oarepo_oai_pmh_harvester.register import Decorators
from oarepo_oai_pmh_harvester.transformer import OAITransformer

# TODO: vytvořit pravidlo na zparcování multilang a vložit ho do jednoho modulu.

@Decorators.rule("xoai")
@Decorators.pre_rule("/dc/description/abstract")
def transform_uk_abstract(paths, el, results, phase, **kwargs):
    abstract = []
    for k, v in el.items():
        if k == "translated":
            abstract.extend(transform_abstract_translated(v))
        else:
            abstract.append(
                {
                    "value": v[0]["value"][0],
                    "lang": get_iso_lang_code(k[:2])
                }
            )
    results[-1]["abstract"] = abstract
    return OAITransformer.PROCESSED


def transform_abstract_translated(el):
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

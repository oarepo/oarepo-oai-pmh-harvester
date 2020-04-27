from invenio_oarepo_oai_pmh_harvester.register import Decorators
from invenio_oarepo_oai_pmh_harvester.transformer import OAITransformer


@Decorators.rule("xoai")
@Decorators.pre_rule("/dc/description/abstract")
def transform_uk_abstract(paths, el, results, phase, **kwargs):
    if "cs" in el:
        results[-1]["abstract"] = [
            {
                "value": el["cs"][0]["cs_CZ"][0]["value"][0],
                "lang": "cze"
            },
            {
                "value": el["en"][0]["en_US"][0]["value"][0],
                "lang": "eng"
            }
        ]
    elif "cs_CZ" in el:
        results[-1]["abstract"] = [
            {
                "value": el["cs_CZ"][0]["value"][0],
                "lang": "cze"
            },
            {
                "value": el["en_US"][0]["value"][0],
                "lang": "eng"
            }
        ]
    else:
        raise ValueError("There is no handler for this option")
    return OAITransformer.PROCESSED

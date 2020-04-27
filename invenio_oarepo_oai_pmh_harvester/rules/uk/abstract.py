from invenio_oarepo_oai_pmh_harvester.register import Decorators
from invenio_oarepo_oai_pmh_harvester.transformer import OAITransformer


@Decorators.rule("xoai")
@Decorators.pre_rule("/dc/description/abstract")
def transform_uk_abstract(self, paths, el, results, phase, **kwargs):
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
    return OAITransformer.PROCESSED

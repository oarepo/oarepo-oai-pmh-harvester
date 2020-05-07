from invenio_oarepo_oai_pmh_harvester.register import Decorators
from invenio_oarepo_oai_pmh_harvester.transformer import OAITransformer


@Decorators.rule("xoai")
@Decorators.pre_rule("/dc/subject")
def transform_subject(paths, el, results, phase, **kwargs):
    # TODO: vyřešit subjects, teď sbíráme jen keywordy
    cz_list = el["cs_CZ"][0]["value"]
    en_list = el["en_US"][0]["value"]
    assert isinstance(cz_list, list)
    assert isinstance(en_list, list)
    keywords = []
    for k in cz_list:
        keywords.append({
            "value": k,
            "lang": "cze"
        })
    for k in en_list:
        keywords.append({
            "value": k,
            "lang": "eng"
        })
    results[-1]["keywords"] = keywords
    return OAITransformer.PROCESSED

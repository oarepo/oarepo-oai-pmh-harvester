from oarepo_oai_pmh_harvester.register import Decorators
from oarepo_oai_pmh_harvester.transformer import OAITransformer


@Decorators.rule("xoai")
@Decorators.pre_rule("/dc/subject")
def transform_subject(paths, el, results, phase, **kwargs):
    # TODO: vyřešit subjects, teď sbíráme jen keywordy
    keywords = []
    cz_keywords = el.get("cs_CZ")
    if cz_keywords:
        cz_list = cz_keywords[0]["value"]
        for k in cz_list:
            if k is None:
                continue
            keywords.append({
                "value": k,
                "lang": "cze"
            })
        assert isinstance(cz_list, list)
    en_keywords = el.get("en_US")
    if en_keywords:
        en_list = en_keywords[0]["value"]
        for k in en_list:
            if k is None:
                continue
            keywords.append({
                "value": k,
                "lang": "eng"
            })
        assert isinstance(en_list, list)
    if keywords:
        results[-1]["keywords"] = keywords
    return OAITransformer.PROCESSED

from oarepo_oai_pmh_harvester.register import Decorators
from oarepo_oai_pmh_harvester.transformer import OAITransformer


@Decorators.rule("xoai")
@Decorators.pre_rule("/dcterms/dateAccepted")
def transform_date_accepted(paths, el, results, phase, **kwargs):
    value = el["value"][0]
    assert len(value) == 1
    results[-1]["dateAccepted"] = value[0]
    return OAITransformer.PROCESSED

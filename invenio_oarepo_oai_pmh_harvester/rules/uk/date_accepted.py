from invenio_oarepo_oai_pmh_harvester.register import Decorators
from invenio_oarepo_oai_pmh_harvester.transformer import OAITransformer


@Decorators.pre_rule("/dcterms/dateAccepted")
def transform_date_accepted(self, paths, el, results, phase, **kwargs):
    value = el["value"][0]
    assert len(value) == 1
    results[-1]["dateAccepted"] = value[0]
    return OAITransformer.PROCESSED

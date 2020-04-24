from invenio_oarepo_oai_pmh_harvester.register import Decorators
from invenio_oarepo_oai_pmh_harvester.transformer import OAITransformer


@Decorators.pre_rule("/thesis/grade")
def transform_grade(self, paths, el, results, phase, **kwargs):
    value = el["cs"][0]["cs_CZ"][0]["value"]
    assert len(value) == 1
    results[-1]["defended"] = get_defended(value[0])
    return OAITransformer.PROCESSED


def get_defended(value):
    dictionary = {
        "Výborně": True,
        "Velmi dobře": True,
        "Prospěl/a": True,
        "Dobře": True,
        "Prospěl": True,
        "Neprospěl": False,
        "Neprospěl/a": False,
        "Výtečně": True,
        "Uspokojivě": True,
        "Dostatečně": True
    }
    return dictionary.get(value)

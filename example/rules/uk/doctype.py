from example.rules.utils import get_ref
from invenio_oarepo_oai_pmh_harvester.register import Decorators
from invenio_oarepo_oai_pmh_harvester.transformer import OAITransformer


@Decorators.rule("xoai")
@Decorators.pre_rule("/dc/type/cs_CZ")
def transform_type(paths, el, results, phase, **kwargs):
    value_ = el["value"]
    assert len(value_) == 1
    results[-1]["doctype"] = get_doc_type(value_[0])
    return OAITransformer.PROCESSED


def get_doc_type(value):
    dictionary = {
        "diplomová práce": "diplomove_prace",
        "bakalářská práce": "bakalarske_prace",
        "dizertační práce": "disertacni_prace",
        "rigorózní práce": "rigorozni_prace"
    }
    slug = dictionary.get(value)
    return get_ref(slug, "doctypes")

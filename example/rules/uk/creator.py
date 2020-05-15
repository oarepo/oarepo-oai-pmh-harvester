from example.rules.utils import iter_array
from invenio_oarepo_oai_pmh_harvester.register import Decorators
from invenio_oarepo_oai_pmh_harvester.transformer import OAITransformer


@Decorators.rule("xoai")
@Decorators.pre_rule("/dc/creator")
def transform_creator(paths, el, results, phase, **kwargs):
    results[-1]["creator"] = [
        {
            "name": x
        } for x in iter_array(el["value"])
    ]

    return OAITransformer.PROCESSED

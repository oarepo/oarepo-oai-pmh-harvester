from invenio_oarepo_oai_pmh_harvester.register import Decorators
from invenio_oarepo_oai_pmh_harvester.rules.utils import iter_array
from invenio_oarepo_oai_pmh_harvester.rules_ import pre_rule
from invenio_oarepo_oai_pmh_harvester.transformer import OAITransformer


@Decorators.pre_rule("/dc/identifier")
def transform_identifier(paths, el, results, phase, **kwargs):
    ids = []
    results[-1]["identifier"] = ids
    return ids


@Decorators.pre_rule("/dc/identifier/uri")
@Decorators.array_value
def transform_identifier_uri(paths, el, results, phase, **kwargs):
    return [
        {
            "type": "originalRecord",
            "value": x
        } for x in iter_array(el["value"])
    ]


@Decorators.pre_rule("/dc/identifier/repId")
def transform_repId(paths, el, results, phase, **kwargs):
    return OAITransformer.PROCESSED


@Decorators.pre_rule("/dc/identifier/aleph")
def transform_aleph(paths, el, results, phase, **kwargs):
    return OAITransformer.PROCESSED


@pre_rule("/others/identifier")
def transform_others_identifier(self, paths, el, results, phase, **kwargs):
    if results[-1].get("identifier") is None:
        results[-1]["identifier"] = [
            {
                "value": el,
                "type": "originalOAI"
            }
        ]
    else:
        results[-1]["identifier"].append(
            {
                "value": el,
                "type": "originalOAI"
            }
        )
    return OAITransformer.PROCESSED

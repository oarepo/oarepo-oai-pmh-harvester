from flask_taxonomies.models import Taxonomy
from invenio_initial_theses_conversion.rules.marc21.bd656 import studyfield_ref

from invenio_oarepo_oai_pmh_harvester.register import Decorators
from invenio_oarepo_oai_pmh_harvester.transformer import OAITransformer


@Decorators.pre_rule("/thesis/degree/discipline")
def transform_degree_discipline(self, paths, el, results, phase, **kwargs):
    value_array = el["cs_CZ"][0]["value"]
    assert len(value_array) == 1
    tax = Taxonomy.get("studyfields")
    results[-1]["studyField"] = studyfield_ref(value_array[0].strip(), tax)["studyField"]
    return OAITransformer.PROCESSED

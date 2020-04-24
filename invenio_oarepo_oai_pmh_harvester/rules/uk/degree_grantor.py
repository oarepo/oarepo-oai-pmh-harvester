from invenio_initial_theses_conversion.rules.marc21.bd7102 import get_degree_grantor

from invenio_oarepo_oai_pmh_harvester.register import Decorators
from invenio_oarepo_oai_pmh_harvester.transformer import OAITransformer


@Decorators.pre_rule("/uk/grantor")
def transform_uk_grantor(self, paths, el, results, phase, **kwargs):
    value_array = el["cs_CZ"][0]["value"]
    assert len(value_array) == 1
    grantor_array = value_array[0].split(",", 3)
    grantor_array = [member.strip() for member in grantor_array]
    results[-1]["degreeGrantor"] = get_degree_grantor(grantor_array[0],
                                                      faculty_name=grantor_array[1],
                                                      department_name=grantor_array[2])
    return OAITransformer.PROCESSED

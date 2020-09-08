from invenio_initial_theses_conversion.rules.marc21.bd7102 import get_degree_grantor

from oarepo_oai_pmh_harvester.register import Decorators
from oarepo_oai_pmh_harvester.transformer import OAITransformer


@Decorators.rule('xoai')
@Decorators.pre_rule("/uk/grantor")
def transform_uk_grantor(paths, el, results, phase, **kwargs):
    cz = el.get("cs_CZ")
    if not cz:
        cz = el.get("cs_CS")
    if not cz:
        return OAITransformer.PROCESSED
    value_array = cz[0]["value"]
    assert len(value_array) == 1
    grantor_array = value_array[0].split(",", 3)
    grantor_array = [member.strip() for member in grantor_array]
    results[-1]["degreeGrantor"] = get_degree_grantor(grantor_array[0],
                                                      faculty_name=grantor_array[1],
                                                      department_name=grantor_array[2])
    return OAITransformer.PROCESSED

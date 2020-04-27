from invenio_oarepo_oai_pmh_harvester.register import Decorators
from invenio_oarepo_oai_pmh_harvester.rules.utils import get_ref, get_iso_lang_code
from invenio_oarepo_oai_pmh_harvester.transformer import OAITransformer


@Decorators.rule('xoai')
@Decorators.pre_rule("/dc/language/iso")
def transform_language_iso(paths, el, results, phase, **kwargs):
    results[-1]["language"] = [get_ref(get_iso_lang_code(el["value"][0][0][:2]), "languages")]
    return OAITransformer.PROCESSED

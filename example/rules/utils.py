from flask_taxonomies.models import Taxonomy
from flask_taxonomies_es.proxies import current_flask_taxonomies_es
from invenio_initial_theses_conversion.rules.utils import get_ref_es
from invenio_initial_theses_conversion.scripts.link import link_self
from pycountry import languages


def get_ref(slug, code):
    res = current_flask_taxonomies_es.get(code, slug)
    if len(res) > 0 and isinstance(res, dict):
        return get_ref_es(res)
    tax = Taxonomy.get(code)
    term = tax.get_term(slug)
    if term is None:
        return None
    return {
        "$ref": link_self(tax.slug, term)
    }


def iter_array(x):
    if not isinstance(x, list):
        yield x
    else:
        for _ in x:
            yield from iter_array(_)


def get_iso_lang_code(lang):
    """
    Convert two-digit iso code into three-digit iso code
    :param lang: Two digit iso code
    :return: Three digit iso code
    """
    iso_lang = languages.get(alpha_2=lang)
    if iso_lang is not None:
        if hasattr(iso_lang, "bibliographic"):
            return getattr(iso_lang, "bibliographic")
        else:
            return getattr(iso_lang, "alpha_3")

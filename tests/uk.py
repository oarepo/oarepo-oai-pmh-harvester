from flask_taxonomies.models import Taxonomy
from invenio_initial_theses_conversion.rules.marc21.bd7102 import get_degree_grantor
from pycountry import languages

from flask_taxonomies_es.proxies import current_flask_taxonomies_es
from invenio_initial_theses_conversion.rules.marc21.bd656 import studyfield_ref
from invenio_initial_theses_conversion.rules.utils import get_ref_es
from invenio_initial_theses_conversion.scripts.link import link_self
from invenio_oarepo_oai_pmh_harvester.rules_ import Rules, pre_rule, array_value
from invenio_oarepo_oai_pmh_harvester.transformer import OAITransformer


class UK(Rules):
    @pre_rule("/dc/contributor")
    def transform_contributor(self, paths, el, results, phase, **kwargs):
        contributors = []
        results[-1]["contributor"] = contributors
        return contributors

    @pre_rule("advisor")
    @array_value
    def transform_advisor(self, el=None, results=None, **kwargs):
        value = el["value"]
        assert len(value) == 1
        return {
            "name": value[0],
            "role": get_ref("advisor", "contributor-type")
        }

    @pre_rule("referee")
    @array_value
    def transform_referee(self, el=None, results=None, **kwargs):
        value = el["value"]
        assert len(value) == 1
        return {
            "name": value[0],
            "role": get_ref("referee", "contributor-type")
        }

    @pre_rule("/dc/creator")
    def transform_creator(self, paths, el, results, phase, **kwargs):
        results[-1]["creator"] = [
            {
                "name": x
            } for x in iter_array(el["value"])
        ]

        return OAITransformer.PROCESSED

    @pre_rule("/dc/identifier")
    def transform_identifier(self, paths, el, results, phase, **kwargs):
        ids = []
        results[-1]["identifier"] = ids
        return ids

    @pre_rule("/dc/identifier/uri")
    @array_value
    def transform_identifier_uri(self, paths, el, results, phase, **kwargs):
        return [
            {
                "type": "originalRecord",
                "value": x
            } for x in iter_array(el["value"])
        ]

    @pre_rule("/dc/description/abstract")
    def trasform_abstract(self, paths, el, results, phase, **kwargs):
        results[-1]["abstract"] = [
            {
                "value": value,
                "lang": get_iso_lang_code(lang[:2])
            }
            for lang, values in el.items() for value_dict in values for value in
            value_dict["value"]]
        return OAITransformer.PROCESSED

    @pre_rule("/dc/language/iso")
    def transform_language_iso(self, paths, el, results, phase, **kwargs):
        results[-1]["language"] = [get_ref(get_iso_lang_code(el["value"][0][0][:2]), "languages")]
        return OAITransformer.PROCESSED

    @pre_rule("/dc/title")
    def transform_title(self, paths, el, results, phase, **kwargs):
        title = []
        results[-1]["title"] = title
        return title

    @pre_rule("/dc/title/cs_CZ")
    @array_value
    def transform_title_cz(self, paths, el, results, phase, **kwargs):
        value = el["value"]
        assert len(value) == 1
        return {
            "name": value[0],
            "lang": "cze"
        }

    @pre_rule("/dc/title/translated")
    @array_value
    def transform_title_translated(self, paths, el, results, phase, **kwargs):
        result = []
        for k, v in el.items():
            value_array = v[0]["value"]
            assert len(value_array) == 1
            result.append(
                {
                    "value": value_array[0],
                    "lang": get_iso_lang_code(k[:2])
                }
            )
        return result

    @pre_rule("/dc/type/cs_CZ")
    def transform_type(self, paths, el, results, phase, **kwargs):
        value_ = el["value"]
        assert len(value_) == 1
        results[-1]["doctype"] = get_doc_type(value_[0])
        return OAITransformer.PROCESSED

    @pre_rule("/dcterms/dateAccepted")
    def transform_date_accepted(self, paths, el, results, phase, **kwargs):
        value = el["value"][0]
        assert len(value) == 1
        results[-1]["dateAccepted"] = value[0]
        return OAITransformer.PROCESSED

    @pre_rule("/thesis/degree/discipline")
    def transform_degree_discipline(self, paths, el, results, phase, **kwargs):
        value_array = el["cs_CZ"][0]["value"]
        assert len(value_array) == 1
        tax = Taxonomy.get("studyfields")
        results[-1]["studyField"] = studyfield_ref(value_array[0].strip(), tax)["studyField"]
        return OAITransformer.PROCESSED

    @pre_rule("/thesis/grade")
    def transform_grade(self, paths, el, results, phase, **kwargs):
        value = el["cs"][0]["cs_CZ"][0]["value"]
        assert len(value) == 1
        results[-1]["defended"] = get_defended(value[0])
        return OAITransformer.PROCESSED

    @pre_rule("/uk/abstract")
    def transform_uk_abstract(self, paths, el, results, phase, **kwargs):
        results[-1]["abstract"] = [
            {
                "value": el["cs"][0]["cs_CZ"][0]["value"][0],
                "lang": "cze"
            },
            {
                "value": el["en"][0]["en_US"][0]["value"][0],
                "lang": "eng"
            }
        ]
        return OAITransformer.PROCESSED

    @pre_rule("/uk/grantor")
    def transform_uk_grantor(self, paths, el, results, phase, **kwargs):
        value_array = el["cs_CZ"][0]["value"]
        assert len(value_array) == 1
        grantor_array = value_array[0].split(",", 3)
        grantor_array = [member.strip() for member in grantor_array]
        results[-1]["degreeGrantor"] = get_degree_grantor(grantor_array[0],
                                                          faculty_name=grantor_array[1],
                                                          department_name=grantor_array[2])
        return OAITransformer.PROCESSED

    @pre_rule("/others/identifier")
    def transform_others_identifier(self, paths, el, results, phase, **kwargs):
        results[-1]["identifier"] = [
            {
                "value": el,
                "type": "originalOAI"
            }
        ]
        return OAITransformer.PROCESSED


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


def get_doc_type(value):
    dictionary = {
        "diplomová práce": "diplomove_prace",
        "bakalářská práce": "bakalarske_prace",
        "dizertační práce": "disertacni_prace",
        "rigorózní práce": "rigorozni_prace"
    }
    slug = dictionary.get(value)
    return get_ref(slug, "doctypes")


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

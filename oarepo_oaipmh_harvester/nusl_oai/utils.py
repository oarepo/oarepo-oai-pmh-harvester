import pycountry


def get_alpha2_lang(lang):
    py_lang = pycountry.languages.get(alpha_3=lang) or pycountry.languages.get(
        bibliographic=lang)
    if not py_lang:
        raise LookupError()
    return py_lang.alpha_2

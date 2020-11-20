from oarepo_oai_pmh_harvester.decorators import rule


@rule("uk", "xoai", "/dc/title")
def rule(el, **kwargs):
    value_ = el[0]["value"][0]
    return {"title": value_}

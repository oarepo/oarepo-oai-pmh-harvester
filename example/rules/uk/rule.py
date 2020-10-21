from oarepo_oai_pmh_harvester.proxies import current_oai_client


@current_oai_client.rule("/dc/title", "xoai")
def rule(el, **kwargs):
    value_ = el[0]["value"][0]
    return {"title": value_}

from oarepo_oai_pmh_harvester.proxies import current_oai_client


@current_oai_client.rule("/test/path", "xoai")
def rule():
    return "ahoj"

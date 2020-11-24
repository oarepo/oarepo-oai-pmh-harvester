from oarepo_oai_pmh_harvester.decorators import endpoint_handler


@endpoint_handler("uk", "xoai")
def mapping_handler(data):
    return "recid"

from oarepo_oai_pmh_harvester.decorators import post_processor


@post_processor("uk", "xoai")
def post_processor_1(data):
    return data

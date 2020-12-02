from oarepo_oai_pmh_harvester.decorators import pre_processor


@pre_processor("uk", "xoai")
def pre_processor_1(data):
    return data

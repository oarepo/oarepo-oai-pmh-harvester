from marshmallow import pre_load
from oarepo_runtime.services.schema.marshmallow import BaseRecordSchema


class BaseOaiHarvesterSchema(BaseRecordSchema):
    @pre_load
    def process_transformers(self, data, **kwargs):
        transformers = data.get("transformers")
        batch_size = data.get("batch_size")
        max_records = data.get("max_records")
        if isinstance(transformers, str):
            data["transformers"] = [item.strip() for item in transformers.split(",")]
        if batch_size == "":
            data.pop("batch_size")
        if max_records == "":
            data.pop("max_records")
        return data

    @pre_load
    def process_writers(self, data, **kwargs):
        writers = data.get("writers")
        if isinstance(writers, str):
            data["writers"] = [item.strip() for item in writers.split(",")]
        return data
import marshmallow as ma
from marshmallow import fields as ma_fields
from marshmallow import pre_load
from oarepo_runtime.services.schema.marshmallow import BaseRecordSchema


class OaiHarvesterSchema(BaseRecordSchema):
    class Meta:
        unknown = ma.RAISE

    baseurl = ma_fields.String(required=True)

    batch_size = ma_fields.Integer()

    code = ma_fields.String(required=True)

    comment = ma_fields.String()

    loader = ma_fields.String()

    max_records = ma_fields.Integer()

    metadataprefix = ma_fields.String(required=True)

    name = ma_fields.String(required=True)

    setspecs = ma_fields.String(required=True)

    transformers = ma_fields.List(ma_fields.String(), required=True)

    writer = ma_fields.String()

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

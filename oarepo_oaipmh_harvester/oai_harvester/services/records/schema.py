import marshmallow as ma
from marshmallow import fields as ma_fields
from oarepo_runtime.marshmallow import BaseRecordSchema


class OaiHarvesterSchema(BaseRecordSchema):
    class Meta:
        unknown = ma.RAISE

    baseurl = ma_fields.String()

    batch_size = ma_fields.Integer()

    code = ma_fields.String()

    comment = ma_fields.String()

    loader = ma_fields.String()

    max_records = ma_fields.Integer()

    metadataprefix = ma_fields.String()

    name = ma_fields.String()

    setspecs = ma_fields.String()

    transformers = ma_fields.List(ma_fields.String())

    writer = ma_fields.String()

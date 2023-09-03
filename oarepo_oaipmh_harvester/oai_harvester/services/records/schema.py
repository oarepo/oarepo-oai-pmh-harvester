import marshmallow as ma
from oarepo_runtime.marshmallow import BaseRecordSchema


class OaiHarvesterSchema(BaseRecordSchema):
    class Meta:
        unknown = ma.RAISE

    baseurl = ma.fields.String(required=True)

    batch_size = ma.fields.Integer()

    code = ma.fields.String(required=True)

    comment = ma.fields.String()

    loader = ma.fields.String()

    max_records = ma.fields.Integer()

    metadataprefix = ma.fields.String(required=True)

    name = ma.fields.String(required=True)

    setspecs = ma.fields.String(required=True)

    transformers = ma.fields.List(ma.fields.String(), required=True)

    writer = ma.fields.String()

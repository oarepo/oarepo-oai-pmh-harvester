import marshmallow as ma
from marshmallow import fields as ma_fields
from oarepo_runtime.services.schema.ui import InvenioUISchema


class OaiHarvesterUISchema(InvenioUISchema):
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

    writers = ma_fields.List(ma_fields.String())

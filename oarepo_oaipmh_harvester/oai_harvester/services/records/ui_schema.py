from marshmallow import fields as ma_fields
from oarepo_runtime.ui.marshmallow import InvenioUISchema


class OaiHarvesterUISchema(InvenioUISchema):
    """OaiHarvesterUISchema schema."""

    code = ma_fields.String()
    baseurl = ma_fields.String()
    metadataprefix = ma_fields.String()
    comment = ma_fields.String()
    name = ma_fields.String()
    setspecs = ma_fields.String()
    loader = ma_fields.String()
    transformers = ma_fields.List(ma_fields.String())
    writer = ma_fields.String()
    max_records = ma_fields.Integer()
    batch_size = ma_fields.Integer()

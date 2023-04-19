import marshmallow as ma
from invenio_records_resources.services.records.schema import (
    BaseRecordSchema as InvenioBaseRecordSchema,
)
from marshmallow import fields as ma_fields
from marshmallow import validate as ma_validate
from oarepo_runtime.validation import validate_datetime


class HarvesterSchema(ma.Schema):
    """HarvesterSchema schema."""

    _id = ma_fields.String(data_key="id", attribute="id")
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


class OaiRunSchema(InvenioBaseRecordSchema):
    """OaiRunSchema schema."""

    harvester = ma_fields.Nested(lambda: HarvesterSchema())
    batches = ma_fields.Integer()
    status = ma_fields.String(validate=[ma_validate.OneOf(["R", "O", "W", "E", "I"])])
    warning = ma_fields.String()
    error = ma_fields.String()
    started = ma_fields.String(validate=[validate_datetime])
    finished = ma_fields.String(validate=[validate_datetime])
    duration = ma_fields.Float()

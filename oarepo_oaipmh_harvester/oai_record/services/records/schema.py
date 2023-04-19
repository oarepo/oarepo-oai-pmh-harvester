import marshmallow as ma
from invenio_records_resources.services.records.schema import (
    BaseRecordSchema as InvenioBaseRecordSchema,
)
from marshmallow import fields as ma_fields
from marshmallow import validate as ma_validate
from oarepo_runtime.validation import validate_datetime


class BatchSchema(ma.Schema):
    """BatchSchema schema."""

    _id = ma_fields.String(data_key="id", attribute="id")
    _version = ma_fields.String(data_key="@v", attribute="@v")


class OaiRecordSchema(InvenioBaseRecordSchema):
    """OaiRecordSchema schema."""

    batch = ma_fields.Nested(lambda: BatchSchema())
    local_identifier = ma_fields.String()
    oai_identifier = ma_fields.String()
    datestamp = ma_fields.String(validate=[validate_datetime])
    status = ma_fields.String(validate=[ma_validate.OneOf(["O", "W", "E", "S"])])
    warnings = ma_fields.List(ma_fields.String())
    errors = ma_fields.List(ma_fields.String())
    entry = ma_fields.Raw()
    context = ma_fields.Raw()

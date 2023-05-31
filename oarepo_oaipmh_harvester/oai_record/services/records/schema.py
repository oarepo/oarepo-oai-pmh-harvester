import marshmallow as ma
from marshmallow import fields as ma_fields
from marshmallow import validate as ma_validate
from oarepo_runtime.marshmallow import BaseRecordSchema
from oarepo_runtime.validation import validate_datetime


class OaiRecordSchema(BaseRecordSchema):
    class Meta:
        unknown = ma.RAISE

    batch = ma_fields.Nested(lambda: BatchSchema())

    context = ma_fields.Raw()

    datestamp = ma_fields.String(validate=[validate_datetime])

    entry = ma_fields.Raw()

    errors = ma_fields.List(ma_fields.Nested(lambda: ErrorsItemSchema()))

    harvester = ma_fields.Nested(lambda: BatchSchema())

    local_identifier = ma_fields.String()

    manual = ma_fields.Boolean()

    oai_identifier = ma_fields.String()

    status = ma_fields.String(validate=[ma_validate.OneOf(["O", "W", "E", "S"])])

    warnings = ma_fields.List(ma_fields.String())


class BatchSchema(ma.Schema):
    class Meta:
        unknown = ma.RAISE

    _id = ma_fields.String(data_key="id", attribute="id")

    _version = ma_fields.String(data_key="@v", attribute="@v")


class ErrorsItemSchema(ma.Schema):
    class Meta:
        unknown = ma.RAISE

    error_info = ma_fields.String()

    error_message = ma_fields.String()

    error_type = ma_fields.String()

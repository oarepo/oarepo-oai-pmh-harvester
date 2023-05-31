import marshmallow as ma
from marshmallow import fields as ma_fields
from marshmallow import validate as ma_validate
from oarepo_runtime.marshmallow import BaseRecordSchema
from oarepo_runtime.validation import validate_datetime


class OaiBatchSchema(BaseRecordSchema):
    class Meta:
        unknown = ma.RAISE

    errors = ma_fields.List(ma_fields.Nested(lambda: ErrorsItemSchema()))

    finished = ma_fields.String(validate=[validate_datetime])

    identifiers = ma_fields.List(ma_fields.String())

    manual = ma_fields.Boolean()

    run = ma_fields.Nested(lambda: RunSchema())

    started = ma_fields.String(validate=[validate_datetime])

    status = ma_fields.String(validate=[ma_validate.OneOf(["R", "O", "W", "E", "I"])])


class ErrorsItemSchema(ma.Schema):
    class Meta:
        unknown = ma.RAISE

    error_message = ma_fields.String()

    error_type = ma_fields.String()

    oai_identifier = ma_fields.String()


class RunSchema(ma.Schema):
    class Meta:
        unknown = ma.RAISE

    _id = ma_fields.String(data_key="id", attribute="id")

    _version = ma_fields.String(data_key="@v", attribute="@v")

import marshmallow as ma
from marshmallow import validate as ma_validate
from oarepo_runtime.marshmallow import BaseRecordSchema
from oarepo_runtime.validation import validate_datetime


class OaiBatchSchema(BaseRecordSchema):
    class Meta:
        unknown = ma.RAISE

    errors = ma.fields.List(ma.fields.Nested(lambda: ErrorsItemSchema()))

    finished = ma.fields.String(validate=[validate_datetime])

    identifiers = ma.fields.List(ma.fields.String())

    manual = ma.fields.Boolean()

    run = ma.fields.Nested(lambda: RunSchema(), required=True)

    started = ma.fields.String(validate=[validate_datetime])

    status = ma.fields.String(
        required=True, validate=[ma_validate.OneOf(["R", "O", "W", "E", "I"])]
    )


class ErrorsItemSchema(ma.Schema):
    class Meta:
        unknown = ma.RAISE

    code = ma.fields.String()

    info = ma.fields.Dict()

    location = ma.fields.String()

    message = ma.fields.String()

    oai_identifier = ma.fields.String()


class RunSchema(ma.Schema):
    class Meta:
        unknown = ma.RAISE

    _id = ma.fields.String(data_key="id", attribute="id")

    _version = ma.fields.String(data_key="@v", attribute="@v")

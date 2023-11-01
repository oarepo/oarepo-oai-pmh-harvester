import marshmallow as ma
from marshmallow import Schema
from marshmallow import fields as ma_fields
from marshmallow.fields import String
from marshmallow.validate import OneOf
from oarepo_runtime.services.schema.ui import InvenioUISchema, LocalizedDateTime


class OaiBatchUISchema(InvenioUISchema):
    class Meta:
        unknown = ma.RAISE

    errors = ma_fields.List(ma_fields.Nested(lambda: ErrorsItemUISchema()))

    finished = LocalizedDateTime()

    identifiers = ma_fields.List(ma_fields.String())

    manual = ma_fields.Boolean()

    run = ma_fields.Nested(lambda: RunUISchema(), required=True)

    started = LocalizedDateTime()

    status = ma_fields.String(
        required=True, validate=[OneOf(["R", "O", "W", "E", "I"])]
    )


class ErrorsItemUISchema(Schema):
    class Meta:
        unknown = ma.RAISE

    code = ma_fields.String()

    info = ma_fields.Dict()

    location = ma_fields.String()

    message = ma_fields.String()

    oai_identifier = ma_fields.String()


class RunUISchema(Schema):
    class Meta:
        unknown = ma.INCLUDE

    _id = ma_fields.String(data_key="id", attribute="id")

    _version = String(data_key="@v", attribute="@v")

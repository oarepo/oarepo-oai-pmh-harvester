import marshmallow as ma
from marshmallow import Schema
from marshmallow import fields as ma_fields
from marshmallow.fields import String
from marshmallow.validate import OneOf
from oarepo_runtime.services.schema.ui import InvenioUISchema, LocalizedDateTime


class OaiRecordUISchema(InvenioUISchema):
    class Meta:
        unknown = ma.RAISE

    batch = ma_fields.Nested(lambda: BatchUISchema(), required=True)

    context = ma_fields.Dict()

    datestamp = LocalizedDateTime()

    entry = ma_fields.Dict()

    errors = ma_fields.List(ma_fields.Nested(lambda: ErrorsItemUISchema()))

    harvester = ma_fields.Nested(lambda: BatchUISchema(), required=True)

    local_identifier = ma_fields.String()

    manual = ma_fields.Boolean()

    oai_identifier = ma_fields.String()

    status = ma_fields.String(validate=[OneOf(["O", "W", "E", "S"])])

    warnings = ma_fields.List(ma_fields.String())


class BatchUISchema(Schema):
    class Meta:
        unknown = ma.INCLUDE

    _id = ma_fields.String(data_key="id", attribute="id")

    _version = String(data_key="@v", attribute="@v")


class ErrorsItemUISchema(Schema):
    class Meta:
        unknown = ma.RAISE

    code = ma_fields.String()

    info = ma_fields.Dict()

    location = ma_fields.String()

    message = ma_fields.String()

import marshmallow as ma
from marshmallow import Schema
from marshmallow import fields as ma_fields
from marshmallow.fields import String
from marshmallow.validate import OneOf
from oarepo_runtime.services.schema.ui import InvenioUISchema, LocalizedDateTime


class OaiRunUISchema(InvenioUISchema):
    class Meta:
        unknown = ma.RAISE

    batches = ma_fields.Integer()

    duration = ma_fields.Float()

    error = ma_fields.String()

    finished = LocalizedDateTime()

    harvester = ma_fields.Nested(lambda: HarvesterUISchema(), required=True)

    manual = ma_fields.Boolean()

    started = LocalizedDateTime()

    status = ma_fields.String(validate=[OneOf(["R", "O", "W", "E", "I"])])

    warning = ma_fields.String()


class HarvesterUISchema(Schema):
    class Meta:
        unknown = ma.INCLUDE

    _id = ma_fields.String(data_key="id", attribute="id")

    _version = String(data_key="@v", attribute="@v")

    code = ma_fields.String()

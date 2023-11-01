import marshmallow as ma
from marshmallow import Schema
from marshmallow import fields as ma_fields
from marshmallow.fields import String
from marshmallow.validate import OneOf
from oarepo_runtime.marshmallow import BaseRecordSchema
from oarepo_runtime.services.schema.validation import validate_datetime


class OaiRunSchema(BaseRecordSchema):
    class Meta:
        unknown = ma.RAISE

    batches = ma_fields.Integer()

    duration = ma_fields.Float()

    error = ma_fields.String()

    finished = ma_fields.String(validate=[validate_datetime])

    harvester = ma_fields.Nested(lambda: HarvesterSchema(), required=True)

    manual = ma_fields.Boolean()

    started = ma_fields.String(validate=[validate_datetime])

    status = ma_fields.String(validate=[OneOf(["R", "O", "W", "E", "I"])])

    warning = ma_fields.String()


class HarvesterSchema(Schema):
    class Meta:
        unknown = ma.INCLUDE

    _id = ma_fields.String(data_key="id", attribute="id")

    _version = String(data_key="@v", attribute="@v")

    code = ma_fields.String()

import marshmallow as ma
from marshmallow import fields as ma_fields
from marshmallow.fields import String
from marshmallow.validate import OneOf
from oarepo_runtime.services.schema.marshmallow import BaseRecordSchema, DictOnlySchema
from oarepo_runtime.services.schema.validation import validate_datetime


class OaiRunSchema(BaseRecordSchema):
    class Meta:
        unknown = ma.RAISE

    created_batches = ma_fields.Integer()

    duration = ma_fields.Float()

    errors = ma_fields.Integer()

    finished = ma_fields.String(validate=[validate_datetime])

    finished_batches = ma_fields.Integer()

    harvester = ma_fields.Nested(lambda: HarvesterSchema(), required=True)

    manual = ma_fields.Boolean()

    started = ma_fields.String(validate=[validate_datetime])

    status = ma_fields.String(validate=[OneOf(["R", "O", "W", "E", "I"])])

    title = ma_fields.String()

    total_batches = ma_fields.Integer()

    warnings = ma_fields.Integer()


class HarvesterSchema(DictOnlySchema):
    class Meta:
        unknown = ma.INCLUDE

    _id = ma_fields.String(data_key="id", attribute="id")

    _version = String(data_key="@v", attribute="@v")

    code = ma_fields.String()

    name = ma_fields.String()

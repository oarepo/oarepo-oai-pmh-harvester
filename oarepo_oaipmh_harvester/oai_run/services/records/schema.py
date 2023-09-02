import marshmallow as ma
from marshmallow import validate as ma_validate
from oarepo_runtime.marshmallow import BaseRecordSchema
from oarepo_runtime.validation import validate_datetime


class OaiRunSchema(BaseRecordSchema):
    class Meta:
        unknown = ma.RAISE

    batches = ma.fields.Integer()

    duration = ma.fields.Float()

    error = ma.fields.String()

    finished = ma.fields.String(validate=[validate_datetime])

    harvester = ma.fields.Nested(lambda: HarvesterSchema(), required=True)

    manual = ma.fields.Boolean()

    started = ma.fields.String(validate=[validate_datetime])

    status = ma.fields.String(validate=[ma_validate.OneOf(["R", "O", "W", "E", "I"])])

    warning = ma.fields.String()


class HarvesterSchema(ma.Schema):
    class Meta:
        unknown = ma.RAISE

    _id = ma.fields.String(data_key="id", attribute="id")

    _version = ma.fields.String(data_key="@v", attribute="@v")

    code = ma.fields.String()

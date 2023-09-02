import marshmallow as ma
from marshmallow import validate as ma_validate
from oarepo_runtime.marshmallow import BaseRecordSchema
from oarepo_runtime.validation import validate_datetime


class OaiRecordSchema(BaseRecordSchema):
    class Meta:
        unknown = ma.RAISE

    batch = ma.fields.Nested(lambda: BatchSchema(), required=True)

    context = ma.fields.Dict()

    datestamp = ma.fields.String(validate=[validate_datetime])

    entry = ma.fields.Dict()

    errors = ma.fields.List(ma.fields.Nested(lambda: ErrorsItemSchema()))

    harvester = ma.fields.Nested(lambda: BatchSchema(), required=True)

    local_identifier = ma.fields.String()

    manual = ma.fields.Boolean()

    oai_identifier = ma.fields.String()

    status = ma.fields.String(validate=[ma_validate.OneOf(["O", "W", "E", "S"])])

    warnings = ma.fields.List(ma.fields.String())


class BatchSchema(ma.Schema):
    class Meta:
        unknown = ma.RAISE

    _id = ma.fields.String(data_key="id", attribute="id")

    _version = ma.fields.String(data_key="@v", attribute="@v")


class ErrorsItemSchema(ma.Schema):
    class Meta:
        unknown = ma.RAISE

    code = ma.fields.String()

    info = ma.fields.Dict()

    location = ma.fields.String()

    message = ma.fields.String()

import marshmallow as ma
from marshmallow import fields as ma_fields
from marshmallow.fields import String
from marshmallow.validate import OneOf
from oarepo_runtime.services.schema.marshmallow import BaseRecordSchema, DictOnlySchema
from oarepo_runtime.services.schema.validation import validate_datetime


class OaiBatchSchema(BaseRecordSchema):
    class Meta:
        unknown = ma.RAISE

    finished = ma_fields.String(validate=[validate_datetime])

    harvester = ma_fields.Nested(lambda: HarvesterSchema())

    manual = ma_fields.Boolean()

    records = ma_fields.List(ma_fields.Nested(lambda: RecordsItemSchema()))

    run = ma_fields.Nested(lambda: RunSchema(), required=True)

    sequence = ma_fields.Integer()

    started = ma_fields.String(validate=[validate_datetime])

    status = ma_fields.String(
        required=True, validate=[OneOf(["R", "O", "W", "E", "I"])]
    )


class RecordsItemSchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    errors = ma_fields.List(ma_fields.Nested(lambda: ErrorsItemSchema()))

    local_error_identifier = ma_fields.String()

    local_record_identifier = ma_fields.String()

    oai_identifier = ma_fields.String()

    title = ma_fields.String()

    url = ma_fields.String()


class ErrorsItemSchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    code = ma_fields.String()

    info = ma_fields.Dict()

    location = ma_fields.String()

    message = ma_fields.String()


class HarvesterSchema(DictOnlySchema):
    class Meta:
        unknown = ma.INCLUDE

    _id = ma_fields.String(data_key="id", attribute="id")

    _version = String(data_key="@v", attribute="@v")

    code = ma_fields.String()

    name = ma_fields.String()


class RunSchema(DictOnlySchema):
    class Meta:
        unknown = ma.INCLUDE

    _id = ma_fields.String(data_key="id", attribute="id")

    _version = String(data_key="@v", attribute="@v")

    started = ma_fields.String(validate=[validate_datetime])

    title = ma_fields.String()

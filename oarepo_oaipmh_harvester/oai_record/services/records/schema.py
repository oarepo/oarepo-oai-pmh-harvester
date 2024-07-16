import marshmallow as ma
from marshmallow import fields as ma_fields
from marshmallow.fields import String
from oarepo_runtime.services.schema.marshmallow import DictOnlySchema
from oarepo_runtime.services.schema.validation import validate_datetime

from oarepo_oaipmh_harvester.common.services.records.oai_record import (
    BaseOaiRecordSchema,
)


class OaiRecordSchema(BaseOaiRecordSchema):
    class Meta:
        unknown = ma.RAISE

    batch = ma_fields.Nested(lambda: BatchSchema(), required=True)

    context = ma_fields.Dict()

    datestamp = ma_fields.String(validate=[validate_datetime])

    entry = ma_fields.Dict()

    errors = ma_fields.List(ma_fields.Nested(lambda: ErrorsItemSchema()))

    harvester = ma_fields.Nested(lambda: HarvesterSchema(), required=True)

    local_identifier = ma_fields.String()

    manual = ma_fields.Boolean()

    oai_identifier = ma_fields.String()

    run = ma_fields.Nested(lambda: RunSchema(), required=True)

    title = ma_fields.String()


class BatchSchema(DictOnlySchema):
    class Meta:
        unknown = ma.INCLUDE

    _id = ma_fields.String(data_key="id", attribute="id")

    _version = String(data_key="@v", attribute="@v")

    sequence = ma_fields.Integer()

    started = ma_fields.String(validate=[validate_datetime])


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

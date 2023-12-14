import marshmallow as ma
from marshmallow import fields as ma_fields
from marshmallow.fields import String
from marshmallow.validate import OneOf
from oarepo_runtime.services.schema.marshmallow import DictOnlySchema
from oarepo_runtime.services.schema.ui import InvenioUISchema, LocalizedDateTime


class OaiBatchUISchema(InvenioUISchema):
    class Meta:
        unknown = ma.RAISE

    finished = LocalizedDateTime()

    harvester = ma_fields.Nested(lambda: HarvesterUISchema())

    manual = ma_fields.Boolean()

    records = ma_fields.List(ma_fields.Nested(lambda: RecordsItemUISchema()))

    run = ma_fields.Nested(lambda: RunUISchema(), required=True)

    sequence = ma_fields.Integer()

    started = LocalizedDateTime()

    status = ma_fields.String(
        required=True, validate=[OneOf(["R", "O", "W", "E", "I"])]
    )


class RecordsItemUISchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    errors = ma_fields.List(ma_fields.Nested(lambda: ErrorsItemUISchema()))

    local_error_identifier = ma_fields.String()

    local_record_identifier = ma_fields.String()

    oai_identifier = ma_fields.String()

    title = ma_fields.String()

    url = ma_fields.String()


class ErrorsItemUISchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    code = ma_fields.String()

    info = ma_fields.Dict()

    location = ma_fields.String()

    message = ma_fields.String()


class HarvesterUISchema(DictOnlySchema):
    class Meta:
        unknown = ma.INCLUDE

    _id = ma_fields.String(data_key="id", attribute="id")

    _version = String(data_key="@v", attribute="@v")

    code = ma_fields.String()

    name = ma_fields.String()


class RunUISchema(DictOnlySchema):
    class Meta:
        unknown = ma.INCLUDE

    _id = ma_fields.String(data_key="id", attribute="id")

    _version = String(data_key="@v", attribute="@v")

    started = LocalizedDateTime()

    title = ma_fields.String()

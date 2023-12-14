import marshmallow as ma
from marshmallow import fields as ma_fields
from marshmallow.fields import String
from oarepo_runtime.services.schema.marshmallow import DictOnlySchema
from oarepo_runtime.services.schema.ui import InvenioUISchema, LocalizedDateTime


class OaiRecordUISchema(InvenioUISchema):
    class Meta:
        unknown = ma.RAISE

    batch = ma_fields.Nested(lambda: BatchUISchema(), required=True)

    context = ma_fields.Dict()

    datestamp = LocalizedDateTime()

    entry = ma_fields.Dict()

    errors = ma_fields.List(ma_fields.Nested(lambda: ErrorsItemUISchema()))

    harvester = ma_fields.Nested(lambda: HarvesterUISchema(), required=True)

    local_identifier = ma_fields.String()

    manual = ma_fields.Boolean()

    oai_identifier = ma_fields.String()

    run = ma_fields.Nested(lambda: RunUISchema(), required=True)

    title = ma_fields.String()


class BatchUISchema(DictOnlySchema):
    class Meta:
        unknown = ma.INCLUDE

    _id = ma_fields.String(data_key="id", attribute="id")

    _version = String(data_key="@v", attribute="@v")

    sequence = ma_fields.Integer()

    started = LocalizedDateTime()


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

import marshmallow as ma
from marshmallow import fields as ma_fields
from marshmallow import validate as ma_validate
from oarepo_runtime.ui import marshmallow as l10n
from oarepo_runtime.ui.marshmallow import InvenioUISchema


class OaiBatchUISchema(InvenioUISchema):
    class Meta:
        unknown = ma.RAISE

    errors = ma_fields.List(ma_fields.Nested(lambda: ErrorsItemUISchema()))

    finished = l10n.LocalizedDateTime()

    identifiers = ma_fields.List(ma_fields.String())

    manual = ma_fields.Boolean()

    run = ma_fields.Nested(lambda: RunUISchema())

    started = l10n.LocalizedDateTime()

    status = ma_fields.String(validate=[ma_validate.OneOf(["R", "O", "W", "E", "I"])])


class ErrorsItemUISchema(ma.Schema):
    class Meta:
        unknown = ma.RAISE

    error_message = ma_fields.String()

    error_type = ma_fields.String()

    oai_identifier = ma_fields.String()


class RunUISchema(ma.Schema):
    class Meta:
        unknown = ma.RAISE

    _id = ma_fields.String(data_key="id", attribute="id")

    _version = ma_fields.String(data_key="@v", attribute="@v")

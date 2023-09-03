import marshmallow as ma
from marshmallow import validate as ma_validate
from oarepo_runtime.ui import marshmallow as l10n
from oarepo_runtime.ui.marshmallow import InvenioUISchema


class OaiBatchUISchema(InvenioUISchema):
    class Meta:
        unknown = ma.RAISE

    errors = ma.fields.List(ma.fields.Nested(lambda: ErrorsItemUISchema()))

    finished = l10n.LocalizedDateTime()

    identifiers = ma.fields.List(ma.fields.String())

    manual = ma.fields.Boolean()

    run = ma.fields.Nested(lambda: RunUISchema(), required=True)

    started = l10n.LocalizedDateTime()

    status = ma.fields.String(
        required=True, validate=[ma_validate.OneOf(["R", "O", "W", "E", "I"])]
    )


class ErrorsItemUISchema(ma.Schema):
    class Meta:
        unknown = ma.RAISE

    code = ma.fields.String()

    info = ma.fields.Dict()

    location = ma.fields.String()

    message = ma.fields.String()

    oai_identifier = ma.fields.String()


class RunUISchema(ma.Schema):
    class Meta:
        unknown = ma.RAISE

    _id = ma.fields.String(data_key="id", attribute="id")

    _version = ma.fields.String(data_key="@v", attribute="@v")

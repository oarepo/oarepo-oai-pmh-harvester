import marshmallow as ma
from marshmallow import fields as ma_fields
from marshmallow import validate as ma_validate
from oarepo_runtime.ui import marshmallow as l10n
from oarepo_runtime.ui.marshmallow import InvenioUISchema


class OaiRunUISchema(InvenioUISchema):
    class Meta:
        unknown = ma.RAISE

    batches = ma_fields.Integer()

    duration = ma_fields.Float()

    error = ma_fields.String()

    finished = l10n.LocalizedDateTime()

    harvester = ma_fields.Nested(lambda: HarvesterUISchema())

    manual = ma_fields.Boolean()

    started = l10n.LocalizedDateTime()

    status = ma_fields.String(validate=[ma_validate.OneOf(["R", "O", "W", "E", "I"])])

    warning = ma_fields.String()


class HarvesterUISchema(ma.Schema):
    class Meta:
        unknown = ma.RAISE

    _id = ma_fields.String(data_key="id", attribute="id")

    _version = ma_fields.String(data_key="@v", attribute="@v")

    code = ma_fields.String()

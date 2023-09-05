import marshmallow as ma
from marshmallow import validate as ma_validate
from oarepo_runtime.ui import marshmallow as l10n
from oarepo_runtime.ui.marshmallow import InvenioUISchema


class OaiRunUISchema(InvenioUISchema):
    class Meta:
        unknown = ma.RAISE

    batches = ma.fields.Integer()

    duration = ma.fields.Float()

    error = ma.fields.String()

    finished = l10n.LocalizedDateTime()

    harvester = ma.fields.Nested(lambda: HarvesterUISchema(), required=True)

    manual = ma.fields.Boolean()

    started = l10n.LocalizedDateTime()

    status = ma.fields.String(validate=[ma_validate.OneOf(["R", "O", "W", "E", "I"])])

    warning = ma.fields.String()


class HarvesterUISchema(ma.Schema):
    class Meta:
        unknown = ma.RAISE

    _id = ma.fields.String(data_key="id", attribute="id")

    _version = ma.fields.String(data_key="@v", attribute="@v")

    code = ma.fields.String()

import marshmallow as ma
from marshmallow import validate as ma_validate
from oarepo_runtime.ui import marshmallow as l10n
from oarepo_runtime.ui.marshmallow import InvenioUISchema


class OaiRecordUISchema(InvenioUISchema):
    class Meta:
        unknown = ma.RAISE

    batch = ma.fields.Nested(lambda: BatchUISchema(), required=True)

    context = ma.fields.Dict()

    datestamp = l10n.LocalizedDateTime()

    entry = ma.fields.Dict()

    errors = ma.fields.List(ma.fields.Nested(lambda: ErrorsItemUISchema()))

    harvester = ma.fields.Nested(lambda: BatchUISchema(), required=True)

    local_identifier = ma.fields.String()

    manual = ma.fields.Boolean()

    oai_identifier = ma.fields.String()

    status = ma.fields.String(validate=[ma_validate.OneOf(["O", "W", "E", "S"])])

    warnings = ma.fields.List(ma.fields.String())


class BatchUISchema(ma.Schema):
    class Meta:
        unknown = ma.RAISE

    _id = ma.fields.String(data_key="id", attribute="id")

    _version = ma.fields.String(data_key="@v", attribute="@v")


class ErrorsItemUISchema(ma.Schema):
    class Meta:
        unknown = ma.RAISE

    code = ma.fields.String()

    info = ma.fields.Dict()

    location = ma.fields.String()

    message = ma.fields.String()

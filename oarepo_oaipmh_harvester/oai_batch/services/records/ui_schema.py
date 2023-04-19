import marshmallow as ma
from marshmallow import fields as ma_fields
from oarepo_runtime.ui import marshmallow as l10n
from oarepo_runtime.ui.marshmallow import InvenioUISchema


class RunUISchema(ma.Schema):
    """RunUISchema schema."""

    _id = ma_fields.String(data_key="id", attribute="id")
    _version = ma_fields.String(data_key="@v", attribute="@v")


class ErrorsItemUISchema(ma.Schema):
    """ErrorsItemUISchema schema."""

    oai_identifier = ma_fields.String()
    error = ma_fields.String()


class OaiBatchUISchema(InvenioUISchema):
    """OaiBatchUISchema schema."""

    run = ma_fields.Nested(lambda: RunUISchema())
    status = l10n.LocalizedEnum(value_prefix="oarepo_oaipmh_harvester.oai_batch")
    identifiers = ma_fields.List(ma_fields.String())
    errors = ma_fields.List(ma_fields.Nested(lambda: ErrorsItemUISchema()))
    started = l10n.LocalizedDateTime()
    finished = l10n.LocalizedDateTime()

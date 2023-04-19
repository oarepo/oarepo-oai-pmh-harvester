import marshmallow as ma
from marshmallow import fields as ma_fields
from oarepo_runtime.ui import marshmallow as l10n
from oarepo_runtime.ui.marshmallow import InvenioUISchema


class BatchUISchema(ma.Schema):
    """BatchUISchema schema."""

    _id = ma_fields.String(data_key="id", attribute="id")
    _version = ma_fields.String(data_key="@v", attribute="@v")


class OaiRecordUISchema(InvenioUISchema):
    """OaiRecordUISchema schema."""

    batch = ma_fields.Nested(lambda: BatchUISchema())
    local_identifier = ma_fields.String()
    oai_identifier = ma_fields.String()
    datestamp = l10n.LocalizedDateTime()
    status = l10n.LocalizedEnum(value_prefix="oarepo_oaipmh_harvester.oai_record")
    warnings = ma_fields.List(ma_fields.String())
    errors = ma_fields.List(ma_fields.String())
    entry = ma_fields.Raw()
    context = ma_fields.Raw()

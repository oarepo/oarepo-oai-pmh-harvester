import marshmallow as ma
from invenio_records_resources.services.records.schema import (
    BaseRecordSchema as InvenioBaseRecordSchema,
)
from marshmallow import ValidationError
from marshmallow import fields as ma_fields
from marshmallow import validate as ma_validate
from marshmallow_utils import fields as mu_fields
from marshmallow_utils import schemas as mu_schemas
from oarepo_runtime.ui import marshmallow as l10n
from oarepo_runtime.validation import validate_date, validate_datetime


class BatchUISchema(ma.Schema):
    """BatchUISchema schema."""

    _id = ma_fields.String(data_key="id", attribute="id")
    _version = ma_fields.String(data_key="@v", attribute="@v")


class OaiRecordUISchema(ma.Schema):
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
    _id = ma_fields.String(data_key="id", attribute="id")
    created = l10n.LocalizedDate()
    updated = l10n.LocalizedDate()
    _schema = ma_fields.String(data_key="$schema", attribute="$schema")

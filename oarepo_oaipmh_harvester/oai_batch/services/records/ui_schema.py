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


class RunUISchema(ma.Schema):
    """RunUISchema schema."""

    _id = ma_fields.String(data_key="id", attribute="id")
    _version = ma_fields.String(data_key="@v", attribute="@v")


class ErrorsItemUISchema(ma.Schema):
    """ErrorsItemUISchema schema."""

    oai_identifier = ma_fields.String()
    error = ma_fields.String()


class OaiBatchUISchema(ma.Schema):
    """OaiBatchUISchema schema."""

    run = ma_fields.Nested(lambda: RunUISchema())
    status = l10n.LocalizedEnum(value_prefix="oarepo_oaipmh_harvester.oai_batch")
    identifiers = ma_fields.List(ma_fields.String())
    errors = ma_fields.List(ma_fields.Nested(lambda: ErrorsItemUISchema()))
    started = l10n.LocalizedDateTime()
    finished = l10n.LocalizedDateTime()
    _id = ma_fields.String(data_key="id", attribute="id")
    created = l10n.LocalizedDate()
    updated = l10n.LocalizedDate()
    _schema = ma_fields.String(data_key="$schema", attribute="$schema")

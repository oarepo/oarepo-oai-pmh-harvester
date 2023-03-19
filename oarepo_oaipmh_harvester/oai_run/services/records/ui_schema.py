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


class HarvesterUISchema(ma.Schema):
    """HarvesterUISchema schema."""

    _id = ma_fields.String(data_key="id", attribute="id")
    code = ma_fields.String()
    baseurl = ma_fields.String()
    metadataprefix = ma_fields.String()
    comment = ma_fields.String()
    name = ma_fields.String()
    setspecs = ma_fields.String()
    loader = ma_fields.String()
    transformers = ma_fields.List(ma_fields.String())
    writer = ma_fields.String()
    max_records = ma_fields.Integer()
    batch_size = ma_fields.Integer()
    created = l10n.LocalizedDate()
    updated = l10n.LocalizedDate()
    _schema = ma_fields.String(data_key="$schema", attribute="$schema")


class OaiRunUISchema(ma.Schema):
    """OaiRunUISchema schema."""

    harvester = ma_fields.Nested(lambda: HarvesterUISchema())
    batches = ma_fields.Integer()
    status = l10n.LocalizedEnum(value_prefix="oarepo_oaipmh_harvester.oai_run")
    warning = ma_fields.String()
    error = ma_fields.String()
    started = l10n.LocalizedDateTime()
    finished = l10n.LocalizedDateTime()
    duration = ma_fields.Float()
    _id = ma_fields.String(data_key="id", attribute="id")
    created = l10n.LocalizedDate()
    updated = l10n.LocalizedDate()
    _schema = ma_fields.String(data_key="$schema", attribute="$schema")

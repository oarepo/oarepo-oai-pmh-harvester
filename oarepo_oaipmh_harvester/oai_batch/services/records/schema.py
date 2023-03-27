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


class RunSchema(ma.Schema):
    """RunSchema schema."""

    _id = ma_fields.String(data_key="id", attribute="id")
    _version = ma_fields.String(data_key="@v", attribute="@v")


class ErrorsItemSchema(ma.Schema):
    """ErrorsItemSchema schema."""

    oai_identifier = ma_fields.String()
    error = ma_fields.String()


class OaiBatchSchema(InvenioBaseRecordSchema):
    """OaiBatchSchema schema."""

    run = ma_fields.Nested(lambda: RunSchema())
    status = ma_fields.String(validate=[ma_validate.OneOf(["R", "O", "W", "E", "I"])])
    identifiers = ma_fields.List(ma_fields.String())
    errors = ma_fields.List(ma_fields.Nested(lambda: ErrorsItemSchema()))
    started = ma_fields.String(validate=[validate_datetime])
    finished = ma_fields.String(validate=[validate_datetime])
    created = ma_fields.String(validate=[validate_date("%Y-%m-%d")], dump_only=True)
    updated = ma_fields.String(validate=[validate_date("%Y-%m-%d")], dump_only=True)
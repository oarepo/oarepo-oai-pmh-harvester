
import marshmallow as ma
import marshmallow.fields as ma_fields
import marshmallow.validate as ma_valid
from invenio_records_resources.services.records.schema import \
    BaseRecordSchema as InvenioBaseRecordSchema
from marshmallow import ValidationError
from marshmallow import validates as ma_validates


class OaipmhRecordMetadataSchema(ma.Schema, ):
    """OaipmhRecordMetadataSchema schema."""










class OaipmhRecordSchema(ma.Schema, ):
    """OaipmhRecordSchema schema."""

    metadata = ma_fields.Raw()

    id = ma_fields.String()

    created = ma_fields.Date()

    updated = ma_fields.Date()

    _schema = ma_fields.String(data_key='$schema')


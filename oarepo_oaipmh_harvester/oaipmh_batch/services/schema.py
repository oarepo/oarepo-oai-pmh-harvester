





import marshmallow as ma
import marshmallow.fields as ma_fields
import marshmallow.validate as ma_valid
from invenio_records_resources.services.records.schema import \
    BaseRecordSchema as InvenioBaseRecordSchema
from marshmallow import ValidationError
from marshmallow import validates as ma_validates


class OaipmhBatchMetadataSchema(ma.Schema, ):
    """OaipmhBatchMetadataSchema schema."""
    
    run_id = ma_fields.String()
    
    status = ma_fields.String(validate=[ma_valid.OneOf(["R", "F", "W", "F", "I"])])
    
    exception = ma_fields.String()
    
    started = ma_fields.Date()
    
    finished = ma_fields.Date()
    
    







class OaipmhBatchSchema(ma.Schema, ):
    """OaipmhBatchSchema schema."""
    
    metadata = ma_fields.Nested(lambda: OaipmhBatchMetadataSchema())
    
    id = ma_fields.String()
    
    created = ma_fields.Date()
    
    updated = ma_fields.Date()
    
    _schema = ma_fields.String(data_key='$schema')
    
    
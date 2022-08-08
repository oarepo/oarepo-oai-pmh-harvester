
import marshmallow as ma
import marshmallow.fields as ma_fields
import marshmallow.validate as ma_valid
from invenio_records_resources.services.records.schema import \
    BaseRecordSchema as InvenioBaseRecordSchema
from marshmallow import ValidationError
from marshmallow import validates as ma_validates


class OaipmhConfigMetadataSchema(ma.Schema, ):
    """OaipmhConfigMetadataSchema schema."""

    code = ma_fields.String()

    baseurl = ma_fields.String(default='')

    metadataprefix = ma_fields.String(default='oai_dc')

    comment = ma_fields.String()

    name = ma_fields.String()

    setspecs = ma_fields.String()

    parser = ma_fields.String()

    transformer = ma_fields.String()

    max_records = ma_fields.Integer(default=50000000)

    batch_size = ma_fields.Integer(default=50)









class OaipmhConfigSchema(ma.Schema, ):
    """OaipmhConfigSchema schema."""

    metadata = ma_fields.Nested(lambda: OaipmhConfigMetadataSchema())

    id = ma_fields.String()

    created = ma_fields.Date()

    updated = ma_fields.Date()

    # _schema = ma_fields.Raw()
    _schema = ma_fields.String(data_key='$schema')


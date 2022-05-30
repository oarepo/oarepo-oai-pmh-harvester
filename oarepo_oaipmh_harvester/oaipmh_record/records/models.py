from invenio_db import db
from invenio_records.models import RecordMetadataBase


class OaipmhRecordMetadata(db.Model, RecordMetadataBase):
    """Model for OaipmhRecordRecord metadata."""

    __tablename__ = "oaipmhrecord_metadata"

    # Enables SQLAlchemy-Continuum versioning
    __versioned__ = {}
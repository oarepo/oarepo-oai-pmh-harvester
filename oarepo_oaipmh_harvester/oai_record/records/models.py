from invenio_db import db
from invenio_records.models import RecordMetadataBase


class OaiRecordMetadata(db.Model, RecordMetadataBase):
    """Model for OaiRecord metadata."""

    __tablename__ = "oairecord_metadata"

    # Enables SQLAlchemy-Continuum versioning
    __versioned__ = {}

from invenio_db import db
from invenio_records.models import RecordMetadataBase


class OaipmhBatchMetadata(db.Model, RecordMetadataBase):
    """Model for OaipmhBatchRecord metadata."""

    __tablename__ = "oaipmhbatch_metadata"

    # Enables SQLAlchemy-Continuum versioning
    __versioned__ = {}
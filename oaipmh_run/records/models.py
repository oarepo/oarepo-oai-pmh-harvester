from invenio_db import db
from invenio_records.models import RecordMetadataBase


class OaipmhRunMetadata(db.Model, RecordMetadataBase):
    """Model for OaipmhRunRecord metadata."""

    __tablename__ = "oaipmhrun_metadata"

    # Enables SQLAlchemy-Continuum versioning
    __versioned__ = {}
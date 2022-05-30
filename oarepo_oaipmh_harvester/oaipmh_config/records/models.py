from invenio_db import db
from invenio_records.models import RecordMetadataBase


class OaipmhConfigMetadata(db.Model, RecordMetadataBase):
    """Model for OaipmhConfigRecord metadata."""

    __tablename__ = "oaipmhconfig_metadata"

    # Enables SQLAlchemy-Continuum versioning
    __versioned__ = {}
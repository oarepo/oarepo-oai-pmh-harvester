from invenio_db import db
from invenio_records.models import RecordMetadataBase


class NrThesesMetadataMetadata(db.Model, RecordMetadataBase):
    """Model for NrThesesMetadataRecord metadata."""

    __tablename__ = "nrthesesmetadata_metadata"

    # Enables SQLAlchemy-Continuum versioning
    __versioned__ = {}

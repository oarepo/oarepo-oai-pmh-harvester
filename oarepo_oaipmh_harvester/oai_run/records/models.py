from invenio_db import db
from invenio_records.models import RecordMetadataBase


class OaiRunMetadata(db.Model, RecordMetadataBase):
    """Model for OaiRunRecord metadata."""

    __tablename__ = "oai_run_metadata"

    # Enables SQLAlchemy-Continuum versioning
    __versioned__ = {}

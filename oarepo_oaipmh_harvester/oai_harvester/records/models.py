from invenio_db import db
from invenio_records.models import RecordMetadataBase


class OaiHarvesterMetadata(db.Model, RecordMetadataBase):
    """Model for OaiHarvesterRecord metadata."""

    __tablename__ = "oai_harvester_metadata"

    # Enables SQLAlchemy-Continuum versioning
    __versioned__ = {}

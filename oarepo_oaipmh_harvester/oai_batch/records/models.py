from invenio_db import db
from invenio_records.models import RecordMetadataBase


class OaiBatchMetadata(db.Model, RecordMetadataBase):
    """Model for OaiBatchRecord metadata."""

    __tablename__ = "oaibatch_metadata"

    # Enables SQLAlchemy-Continuum versioning
    __versioned__ = {}

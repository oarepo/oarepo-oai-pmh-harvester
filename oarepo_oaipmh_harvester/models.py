import uuid
from typing import TYPE_CHECKING, Any

from invenio_db import db
from sqlalchemy.dialects import postgresql
from sqlalchemy_utils.types import JSONType, UUIDType

if TYPE_CHECKING:
    db: Any  # type: ignore[no-redef]


class OAIHarvesterRun(db.Model):
    """Run of an OAI harvester."""

    __tablename__ = "oai_harvest_runs"

    id = db.Column(
        UUIDType,
        primary_key=True,
        default=uuid.uuid4,
    )
    """Record identifier."""
    """ID of the run."""

    harvester_id = db.Column(db.String(255), nullable=False)
    """Persistent ID of the harvester."""

    manual = db.Column(db.Boolean, default=False, nullable=False)
    """True if the run was started manually - for example user reindexes a single record."""

    title = db.Column(db.String(255), nullable=True)
    """Title of the run."""

    harvester_config = db.Column(
        db.JSON()
        .with_variant(
            postgresql.JSONB(none_as_null=True),
            "postgresql",
        )
        .with_variant(
            JSONType(),
            "sqlite",
        )
        .with_variant(
            JSONType(),
            "mysql",
        ),
        default=lambda: dict(),
        nullable=False,
    )
    """Configuration of the harvester for this run - just for audit purposes."""

    start_time = db.Column(db.DateTime, nullable=False)
    """Start time of the run."""

    end_time = db.Column(db.DateTime, nullable=True)
    """End time of the run."""

    last_update_time = db.Column(db.DateTime, nullable=True)
    """Last update time of the run."""

    status = db.Column(db.String(10), nullable=False)
    """Status of the run:
    
    - 'running': the run is still running
    - 'finishing': the run is finishing 
        (an empty batch was received, but some of the workers might still be running)
    - 'stopped': the run was stopped
    - 'finished': the run has finished successfully
    - 'failed': the run has failed
    """

    records = db.Column(
        db.Integer,
        default=0,
        nullable=False,
    )
    """Number of records harvested during the run (including not changed, deleted, ...)."""

    finished_records = db.Column(
        db.Integer,
        default=0,
        nullable=False,
    )
    """Number of records that were finished during the run (including not changed, deleted, ...)."""

    ok_records = db.Column(
        db.Integer,
        default=0,
        nullable=False,
    )
    """Number of records that were successfully harvested during the run."""

    failed_records = db.Column(
        db.Integer,
        default=0,
        nullable=False,
    )
    """Number of records that failed during the run."""


class OAIHarvestedRecord(db.Model):
    """Metadata about a harvested record. Always contains the latest metadata"""

    __tablename__ = "oai_harvest_records"

    oai_identifier = db.Column(db.String(255), primary_key=True)
    """OAI identifier of the record."""

    record_id = db.Column(db.String(255), nullable=True)
    """Record identifier of the record (local identifier)."""

    datestamp = db.Column(db.DateTime, nullable=False)
    """Datestamp of the record."""

    harvested_at = db.Column(db.DateTime, nullable=False)
    """Time when the record was harvested."""

    deleted = db.Column(db.Boolean, default=False, nullable=False)
    """True if the record was deleted during the harvest."""

    has_errors = db.Column(db.Boolean, default=False, nullable=False)
    """True if the record has errors during the harvest."""

    has_warnings = db.Column(db.Boolean, default=False, nullable=False)
    """True if the record has warnings during the harvest."""

    errors = db.Column(
        db.JSON()
        .with_variant(
            postgresql.JSONB(none_as_null=True),
            "postgresql",
        )
        .with_variant(
            JSONType(),
            "sqlite",
        )
        .with_variant(
            JSONType(),
            "mysql",
        ),
        default=lambda: dict(),
        nullable=False,
    )
    """Errors."""

    original_data = db.Column(
        db.JSON()
        .with_variant(
            postgresql.JSONB(none_as_null=True),
            "postgresql",
        )
        .with_variant(
            JSONType(),
            "sqlite",
        )
        .with_variant(
            JSONType(),
            "mysql",
        ),
        default=lambda: dict(),
        nullable=False,
    )
    """Original data."""

    transformed_data = db.Column(
        db.JSON()
        .with_variant(
            postgresql.JSONB(none_as_null=True),
            "postgresql",
        )
        .with_variant(
            JSONType(),
            "sqlite",
        )
        .with_variant(
            JSONType(),
            "mysql",
        ),
        default=lambda: dict(),
        nullable=False,
    )
    """Transformed data before they were stored into the target record."""

    run_id = db.Column(UUIDType, db.ForeignKey("oai_harvest_runs.id"), nullable=False)
    """ID of the run during which the record was harvested."""

    run = db.relationship(
        "OAIHarvesterRun",
        backref="harvested_records",
        foreign_keys=[run_id],
    )

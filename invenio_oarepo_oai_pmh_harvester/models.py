import uuid

from invenio_db import db
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import backref, relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy_utils import UUIDType, JSONType


# PARSER_ENTRYPOINT_GROUP = "invenio_oarepo_oai_pmh_harvester.parsers"
from invenio_oarepo_oai_pmh_harvester import registry


class OAIRecord(db.Model):
    __tablename__ = "oarepo_oai_record"
    id = db.Column(
        UUIDType,
        ForeignKey('records_metadata.id'),
        primary_key=True,
        default=uuid.uuid4,
    )
    oai_identifier = db.Column(
        db.String(2048),
        unique=True,
        nullable=False
    )
    last_sync_id = db.Column(
        db.INTEGER(),
        ForeignKey('oarepo_oai_sync.id'),
        nullable=True
    )
    modification_sync_id = db.Column(
        db.INTEGER(),
        ForeignKey('oarepo_oai_sync.id'),
        nullable=True
    )
    creation_sync_id = db.Column(
        db.INTEGER(),
        ForeignKey('oarepo_oai_sync.id'),
        nullable=True
    )
    timestamp = db.Column(db.TIMESTAMP, nullable=False)
    metadata_record = relationship(
        "RecordMetadata",
        backref=backref("oarepo_oai_record", uselist=False)
    )


class OAISync(db.Model):
    __tablename__ = "oarepo_oai_sync"
    id = db.Column(db.Integer, primary_key=True)
    provider_id = db.Column(db.Integer, ForeignKey('oarepo_oai_provider.id'))
    sync_start = db.Column(db.TIMESTAMP)
    sync_end = db.Column(db.TIMESTAMP)
    status = db.Column(db.String(32))
    logs = db.Column(db.String(2048))

    # number of created, modified and deleted records for statistics
    rec_created = db.Column(db.Integer)
    rec_modified = db.Column(db.Integer)
    rec_deleted = db.Column(db.Integer)
    provider = relationship(
        "OAIProvider",
        backref=backref("synchronizations")
    )


class OAIProvider(db.Model):
    __tablename__ = "oarepo_oai_provider"
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(16), nullable=False, unique=True)
    description = db.Column(db.String(2048), nullable=True)
    oai_endpoint = db.Column(db.String(2048), nullable=False)
    set_ = db.Column(db.String(256), name="set")
    metadata_prefix = db.Column(db.String(32), default="oai_dc")
    constant_fields = db.Column(
        db.JSON().with_variant(
            postgresql.JSONB(none_as_null=True),
            'postgresql',
        ).with_variant(
            JSONType(),
            'sqlite',
        ).with_variant(
            JSONType(),
            'mysql',
        ),
        default=lambda: dict(),
        nullable=True
    )
    parsers = registry.parsers.get(code) or {}
    rules = registry.rules.get(code) or {}
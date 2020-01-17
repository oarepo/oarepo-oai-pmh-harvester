import uuid

import pkg_resources
from invenio_db import db
from sqlalchemy import Table
from sqlalchemy.orm import backref, relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy_utils import UUIDType
from werkzeug.utils import cached_property

PARSER_ENTRYPOINT_GROUP = "invenio_oarepo_oai_pmh_harvester.parsers"

oarepo_oai_provider_rules = Table(
    'oarepo_oai_provider_rules', db.metadata,
    db.Column('provider_id', db.Integer, ForeignKey('oarepo_oai_provider.id')),
    db.Column('rule_id', db.Integer, ForeignKey('oarepo_oai_rule.id'))
)


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


class OAIParser(db.Model):
    __tablename__ = "oarepo_oai_parser"
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(16), nullable=False, unique=True)
    description = db.Column(db.String(2048), nullable=True)
    entry_point = db.Column(db.String(256))


class OAIRule(db.Model):
    __tablename__ = "oarepo_oai_rule"
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(16), nullable=False, unique=True)
    description = db.Column(db.String(2048), nullable=True)
    entry_point = db.Column(db.String(256))


class OAIProvider(db.Model):
    __tablename__ = "oarepo_oai_provider"
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(16), nullable=False, unique=True)
    description = db.Column(db.String(2048), nullable=True)
    oai_endpoint = db.Column(db.String(2048), nullable=False)
    metadata_prefix = db.Column(db.String(32), default="oai_dc")
    oai_parser_id = db.Column(db.Integer, ForeignKey('oarepo_oai_parser.id'))
    rules = relationship("OAIRule", secondary=oarepo_oai_provider_rules,
                         backref="providers")
    oai_parser = relationship(
        "OAIParser",
        backref=backref("providers"))

    @cached_property
    def parser_instance(self):
        for entry_point in pkg_resources.iter_entry_points(PARSER_ENTRYPOINT_GROUP):
            if entry_point.name == self.oai_parser.entry_point:
                return entry_point.load()
        raise KeyError(f"Parser with entry_point {self.oai_parser.entry_point} is not available")

import uuid
from functools import lru_cache

import pkg_resources
from invenio_db import db
from sqlalchemy import Table
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import backref, relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy_utils import UUIDType, JSONType
from werkzeug.utils import cached_property

from oarepo_nusl_rules import rule_registry
from oarepo_nusl_rules.exceptions import NotFoundError
from oarepo_oai_parsers import parser_registry

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


class OAIRule(db.Model):
    __tablename__ = "oarepo_oai_rule"
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(16), nullable=False, unique=True)
    description = db.Column(db.String(2048), nullable=True)


class OAIProvider(db.Model):
    __tablename__ = "oarepo_oai_provider"
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(16), nullable=False, unique=True)
    description = db.Column(db.String(2048), nullable=True)
    oai_endpoint = db.Column(db.String(2048), nullable=False)
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
    oai_parser_id = db.Column(db.Integer, ForeignKey('oarepo_oai_parser.id'))
    rules = relationship("OAIRule", secondary=oarepo_oai_provider_rules,
                         backref="providers")
    oai_parser = relationship(
        "OAIParser",
        backref=backref("providers"))

    @cached_property
    def parser_instance(self):
        if self.oai_parser is None:
            raise NotFoundError(
                "Parser has not been found. Please check your providers if contain parser id and "
                "check parsers.")
        parser_code = self.oai_parser.code
        parser_registry.load()
        parser = parser_registry.parsers.get(parser_code)
        if parser is not None:
            return parser
        raise NotFoundError(
            "Parser has not been found. Please check your providers if contain parser id and "
            "check parsers.")

    @cached_property
    def rule_instance(self):
        if self.rules is None:
            raise NotFoundError(
                "Rules has not been found. Please check your providers if contain rules.")
        rule_registry.load()
        return rule_registry


class OAIMapper(db.Model):
    __tablename__ = "oarepo_oai_mapper"
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(2048), unique=True)
    rule_id = db.Column(db.Integer, ForeignKey('oarepo_oai_rule.id'))
    provider_id = db.Column(db.Integer, ForeignKey('oarepo_oai_provider.id'))
    rule = relationship(
        "OAIRule",
        backref=backref("oarepo_oai_mapper", uselist=False)
    )
    provider = relationship(
        "OAIProvider",
        backref=backref("oarepo_oai_mapper")
    )

    @staticmethod
    def parse_rules():
        rule_map = OAIMapper.query.all()
        for _ in rule_map:
            print(_)


class OAIStats(db.Model):
    __tablename__ = "oarepo_oai_stats"
    id = db.Column(db.Integer, primary_key=True)
    provider_id = db.Column(db.Integer, ForeignKey('oarepo_oai_provider.id'))
    sync_start = db.Column(db.TIMESTAMP)
    sync_end = db.Column(db.TIMESTAMP)
    status = db.Column(db.String(32))
    logs = db.Column(db.String(2048))
    result_json = db.Column(
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
    provider = relationship(
        "OAIProvider",
        backref=backref("statistics")
    )

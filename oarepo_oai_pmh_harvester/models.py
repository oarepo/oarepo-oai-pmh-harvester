import uuid

from invenio_db import db
from sqlalchemy.orm import backref, relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy_utils import UUIDType


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
    )
    pid = db.Column(
        db.String(),
        unique=True,
        nullable=False
    )
    last_sync_id = db.Column(
        db.Integer(),
        ForeignKey('oarepo_oai_sync.id'),
        nullable=True
    )
    modification_sync_id = db.Column(
        db.Integer(),
        ForeignKey('oarepo_oai_sync.id'),
        nullable=True
    )
    creation_sync_id = db.Column(
        db.Integer(),
        ForeignKey('oarepo_oai_sync.id'),
        nullable=True
    )
    timestamp = db.Column(db.TIMESTAMP, nullable=False)
    metadata_record = relationship(
        "RecordMetadata",
        backref=backref("oarepo_oai_record", uselist=False)
    )
    oai_identifiers = relationship("OAIIdentifier", backref=backref("oarepo_oai_record"))

    def __repr__(self):
        return f"OAIRecord(id={self.id}, oai_identifier={self.oai_identifier}, pid={self.pid}, " \
               f"last_sync_id={self.last_sync_id}, modification_s" \
               f"ync_id={self.modification_sync_id}, creation_sync_id={self.creation_sync_id}, " \
               f"timestamp={self.timestamp})"

    @classmethod
    def get_record(cls, oai_identifier):
        oai_identifier = OAIIdentifier.query.filter_by(oai_identifier=oai_identifier).one_or_none()
        if not oai_identifier:
            return None
        else:
            return cls.query.get(oai_identifier.oai_record_id)


class OAISync(db.Model):
    __tablename__ = "oarepo_oai_sync"
    id = db.Column(db.Integer, primary_key=True)
    provider_code = db.Column(db.String, nullable=False)
    synchronizer_code = db.Column(db.String)
    purpose = db.Column(db.String)
    sync_start = db.Column(db.TIMESTAMP)
    sync_end = db.Column(db.TIMESTAMP)
    status = db.Column(db.String(32))
    logs = db.Column(db.Text())

    # number of created, modified and deleted records for statistics
    records_created = db.Column(db.Integer)
    records_modified = db.Column(db.Integer)
    records_deleted = db.Column(db.Integer)
    tracebacks = relationship("OAIRecordExc", backref=backref("synchronization"))


class OAIRecordExc(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    oai_identifier = db.Column(db.String, nullable=False)
    traceback = db.Column(db.Text(), nullable=True)
    oai_sync_id = db.Column(db.Integer, ForeignKey('oarepo_oai_sync.id'))


class OAIIdentifier(db.Model):
    __tablename__ = "oarepo_oai_identifiers"
    id = db.Column(db.Integer, primary_key=True)
    oai_record_id = db.Column(UUIDType, ForeignKey('oarepo_oai_record.id'))
    oai_identifier = db.Column(
        db.String(2048),
        unique=True,
        # nullable=False
    )

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
        nullable=False
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

    def __repr__(self):
        return f"OAIRecord(id={self.id}, oai_identifier={self.oai_identifier}, pid={self.pid}, " \
               f"last_sync_id={self.last_sync_id}, modification_s" \
               f"ync_id={self.modification_sync_id}, creation_sync_id={self.creation_sync_id}, " \
               f"timestamp={self.timestamp})"

    @classmethod
    def get_record(cls, oai_identifier):
        return cls.query.filter_by(oai_identifier=oai_identifier).one_or_none()


class OAISync(db.Model):
    __tablename__ = "oarepo_oai_sync"
    id = db.Column(db.Integer, primary_key=True)
    provider_code = db.Column(db.String, nullable=False)
    synchronizer_code = db.Column(db.String)
    sync_start = db.Column(db.TIMESTAMP)
    sync_end = db.Column(db.TIMESTAMP)
    status = db.Column(db.String(32))
    logs = db.Column(db.Text())

    # number of created, modified and deleted records for statistics
    records_created = db.Column(db.Integer)
    records_modified = db.Column(db.Integer)
    records_deleted = db.Column(db.Integer)
    tracebacks = relationship("OAIRecordExc", backref=backref("synchronization"))


# TODO: odstranit a udělat rest api z configu
# class OAISynchronizers(db.Model):
#     __tablename__ = "oarepo_oai_synchronizers"
#     id = db.Column(db.Integer, primary_key=True)
#     provider_id = db.Column(db.Integer, ForeignKey('oarepo_oai_provider.id'))
#     oai_endpoint = db.Column(db.String(2048), nullable=False)
#     set_ = db.Column(db.String(256), name="set")
#     metadata_prefix = db.Column(db.String(32), default="oai_dc")
#     constant_fields = db.Column(
#         db.JSON().with_variant(
#             postgresql.JSONB(none_as_null=True),
#             'postgresql',
#         ).with_variant(
#             JSONType(),
#             'sqlite',
#         ).with_variant(
#             JSONType(),
#             'mysql',
#         ),
#         default=lambda: dict(),
#         nullable=True
#     )
#     unhandled_paths = db.Column(
#         db.JSON().with_variant(
#             postgresql.JSONB(none_as_null=True),
#             'postgresql',
#         ).with_variant(
#             JSONType(),
#             'sqlite',
#         ).with_variant(
#             JSONType(),
#             'mysql',
#         ),
#         nullable=True
#     )
#     default_endpoint = db.Column(db.String(), nullable=False)
#     endpoint_mapping = db.Column(
#         db.JSON().with_variant(
#             postgresql.JSONB(none_as_null=True),
#             'postgresql',
#         ).with_variant(
#             JSONType(),
#             'sqlite',
#         ).with_variant(
#             JSONType(),
#             'mysql',
#         ),
#         nullable=True
#     )


class OAIRecordExc(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    oai_identifier = db.Column(db.String, nullable=False)
    traceback = db.Column(db.Text(), nullable=True)
    oai_sync_id = db.Column(db.Integer, ForeignKey('oarepo_oai_sync.id'))

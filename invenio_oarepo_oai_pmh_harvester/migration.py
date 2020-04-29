from datetime import datetime
from typing import Callable

from invenio_db import db
from invenio_records.models import RecordMetadata
from sqlalchemy.exc import IntegrityError

from invenio_oarepo_oai_pmh_harvester.models import OAIRecord


class OAIMigration:
    def __init__(self, handler: Callable):
        self.handler = handler

    def migrate(self):
        #  https://docs.sqlalchemy.org/en/13/orm/query.html?highlight=yield_per#sqlalchemy.orm
        #  .query.Query.yield_per
        records = RecordMetadata.query.paginate()
        idx = 0
        try:
            while records.has_next:
                records = records.next()
                for record in records.items:
                    oai_record = None
                    idx += 1
                    oai_identifier = self.handler(record.json)
                    if not oai_identifier:
                        print(f'Record "{record.json["id"]}" does not contain oai_id a has been skiped')
                        continue
                    oai_record = OAIRecord.query.filter_by(oai_identifier=oai_identifier).one_or_none()
                    if oai_record:
                        print(f'Record with oai_id "{oai_identifier}" is already existing')
                        continue
                    oai_record = OAIRecord(oai_identifier=oai_identifier, timestamp=datetime.utcnow(),
                                           metadata_record=record)
                    db.session.add(oai_record)
                    print(
                        f'Record with oai_id "{oai_identifier}" and nusl_id "{record.json["id"]}" has '
                        f'been added')
                    # oai_record.metadata_record = record
                    if idx % 100 == 0:
                        db.session.commit()
                        print("Session was commited")
        except IntegrityError:
            db.session.rollback()
        else:
            db.session.commit()
        finally:
            db.session.commit()

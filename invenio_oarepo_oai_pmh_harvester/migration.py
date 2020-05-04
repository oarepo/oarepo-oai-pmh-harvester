from datetime import datetime
from typing import Callable

from invenio_db import db
from invenio_records.models import RecordMetadata
from sqlalchemy.exc import IntegrityError

from invenio_oarepo_oai_pmh_harvester.models import OAIRecord, OAIProvider
from invenio_oarepo_oai_pmh_harvester.oai_base import OAIDBBase


class OAIMigration(OAIDBBase):
    def __init__(self, handler: Callable, provider: OAIProvider):
        super().__init__(provider)
        self.handler = handler

    def synchronize(self):
        records = RecordMetadata.query.paginate()
        idx = 0
        try:
            while_condition = True
            while while_condition:
                for record in records.items:
                    oai_record = None
                    idx += 1
                    oai_identifier = self.handler(record.json)
                    if not oai_identifier: # pragma: no cover
                        print(
                            f'Record "{record.json["id"]}" does not contain oai_id and has been '
                            f'skiped')
                        continue
                    oai_record = OAIRecord.query.filter_by(
                        oai_identifier=oai_identifier).one_or_none()
                    if oai_record: # pragma: no cover
                        print(f'Record with oai_id "{oai_identifier}" is already existing')
                        continue
                    oai_record = OAIRecord(oai_identifier=oai_identifier,
                                           timestamp=datetime.utcnow(),
                                           metadata_record=record)
                    db.session.add(oai_record)
                    print(
                        f'Record with oai_id "{oai_identifier}" and nusl_id "{record.json["id"]}" '
                        f'has '
                        f'been added')
                    if idx % 100 == 0: # pragma: no cover
                        db.session.commit()
                        print("Session was commited")
                while_condition = records.has_next
                records = records.next()
        except IntegrityError: # pragma: no cover
            db.session.rollback()
        else:
            db.session.commit()
        finally:
            db.session.commit()

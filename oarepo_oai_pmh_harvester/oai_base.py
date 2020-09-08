import traceback
from datetime import datetime

from invenio_db import db

from oarepo_oai_pmh_harvester.models import OAIProvider, OAISync


class OAIDBBase:
    def __init__(self, provider: OAIProvider):
        self.provider = provider
        self.deleted = 0
        self.created = 0
        self.modified = 0

    def run(self, start_oai: str = None, start_id: int = None, break_on_error: bool = True):
        """

        :return:
        :rtype:
        """
        with db.session.begin_nested():
            self.oai_sync = OAISync(
                provider=self.provider,
                sync_start=datetime.utcnow(),
                status="active")
            db.session.add(self.oai_sync)
        db.session.commit()
        try:
            self.synchronize(start_oai=start_oai, start_id=start_id, break_on_error=break_on_error)
            self.update_oai_sync("ok")
        except:
            self.update_oai_sync("failed")
            raise
        finally:
            db.session.commit()

    def update_oai_sync(self, status):
        with db.session.begin_nested():
            # self.oai_sync = db.session.merge(self.oai_sync)
            self.oai_sync.status = status
            self.oai_sync.sync_end = datetime.utcnow()
            self.oai_sync.rec_modified = self.modified
            self.oai_sync.rec_created = self.created
            self.oai_sync.rec_deleted = self.deleted
            if status == "failed":
                self.oai_sync.logs = traceback.format_exc()
            db.session.add(self.oai_sync)
        db.session.commit()

    def synchronize(self, start_oai: str = None, start_id: int = None, break_on_error: bool = True):
        pass

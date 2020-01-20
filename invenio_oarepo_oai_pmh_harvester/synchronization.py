import logging
import traceback
from datetime import datetime

from invenio_db import db
from sickle import Sickle

from invenio_oarepo_oai_pmh_harvester.models import (OAIProvider, OAIRecord,
                                                     OAISync)

oai_logger = logging.getLogger(__name__)
oai_logger.setLevel(logging.DEBUG)


class OAISynchronizer:
    """

    """

    def __init__(self, provider: OAIProvider):
        self.provider = provider
        self.oai_sync = None

    def run(self):
        """

        :return:
        :rtype:
        """
        with db.session.begin_nested():
            self.oai_sync = OAISync(provider=self.provider, sync_start=datetime.utcnow())
            db.session.add(self.oai_sync)
        try:
            self.synchronize()
            with db.session.begin_nested():
                self.oai_sync = db.session.merge(self.oai_sync)
                self.oai_sync.status = "ok"
                db.session.add(self.oai_sync)
        except:
            with db.session.begin_nested():
                self.oai_sync = db.session.merge(self.oai_sync)
                self.oai_sync.status = "failed"
                self.oai_sync.log = traceback.format_exc()
                db.session.add(self.oai_sync)
            raise

    def synchronize(self):
        """

        :return:
        :rtype:
        """
        oai_logger.info(f"OAI harvester on endpoint: {self.provider.oai_endpoint} has started!")
        sickle = Sickle(self.provider.oai_endpoint)
        sickle.class_mapping['ListRecords'] = self.provider.parser_instance
        sickle.class_mapping['GetRecord'] = self.provider.parser_instance

        identifiers = sickle.ListIdentifiers(metadataPrefix=self.provider.metadata_prefix)
        for identifier in identifiers:
            datestamp = identifier.datestamp
            oai_identifier = identifier.identifier
            deleted = identifier.deleted
            with db.session.begin_nested():
                if deleted:
                    self.delete(oai_identifier, datestamp)
                else:
                    self.update(oai_identifier, datestamp)

    def update(self, oai_identifier, datestamp):
        """

        :param oai_identifier:
        :type oai_identifier:
        :param datestamp:
        :type datestamp:
        :return:
        :rtype:
        """
        oai_rec = OAIRecord.query.filter_by(oai_identifier=oai_identifier).one_or_none()
        # sem přijdou metadata
        if oai_rec is None:
            record_id = self.create_record(oai_identifier)
            oai_rec = OAIRecord(id=record_id, oai_identifier=oai_identifier,
                                creation_sync_id=self.oai_sync.id)
        else:
            self.update_record(oai_identifier)
            oai_rec.modification_sync_id = self.oai_sync.id
        oai_rec.last_sync_id = self.oai_sync.id
        oai_rec.timestamp = datestamp
        db.session.add(oai_rec)

    def create_record(self, oai_identifier):
        """

        :param oai_identifier:
        :type oai_identifier:
        :return:
        :rtype:
        """
        pass

    def update_record(self, oai_identifier):
        """

        :param oai_identifier:
        :type oai_identifier:
        :return:
        :rtype:
        """
        pass

    def delete(self, oai_identifier, datestamp):
        """

        :param oai_identifier:
        :type oai_identifier:
        :param datestamp:
        :type datestamp:
        :return:
        :rtype:
        """
        pass

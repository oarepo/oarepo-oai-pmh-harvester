import logging
import traceback
from datetime import datetime

from invenio_db import db
from sickle import Sickle

from invenio_oarepo_oai_pmh_harvester.models import (OAIProvider, OAIRecord,
                                                     OAISync, OAIMapper)
from oarepo_nusl_rules import rule_registry

oai_logger = logging.getLogger(__name__)
oai_logger.setLevel(logging.DEBUG)


class OAISynchronizer:
    """

    """

    def __init__(self, provider: OAIProvider):
        self.provider = provider
        self.oai_sync = None
        self.sickle = Sickle(self.provider.oai_endpoint)
        self.sickle.class_mapping['ListRecords'] = self.provider.parser_instance
        self.sickle.class_mapping['GetRecord'] = self.provider.parser_instance

    def run(self):
        """

        :return:
        :rtype:
        """
        with db.session.begin_nested():
            self.oai_sync = OAISync(provider=self.provider, sync_start=datetime.utcnow(),
                                    status="active")
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

        identifiers = self.sickle.ListIdentifiers(metadataPrefix=self.provider.metadata_prefix)
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
        original_record = self.sickle.GetRecord(identifier=oai_identifier,
                                                metadataPrefix=self.provider.metadata_prefix)

        rules_dict = self.provider.rule_instance.rules
        mapper = OAIMapper.query.all()
        print(original_record.xml_dict, rules_dict)
        for _ in mapper:
            rule_function = rules_dict.get(_.rule.code)
            xml_address = original_record.record_map.get(_.address)
            source = original_record.get_dotted_data(xml_address)
            rule_function(source)
            print(rule_function, xml_address, source)


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

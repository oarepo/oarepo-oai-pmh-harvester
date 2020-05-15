import logging
import traceback
from itertools import islice
from typing import Callable, List

import pytz
from dateutil.parser import isoparse
from invenio_db import db
from invenio_records.models import RecordMetadata
from sickle import Sickle
from sickle.oaiexceptions import IdDoesNotExist

from invenio_nusl_theses.proxies import nusl_theses
from invenio_oarepo_oai_pmh_harvester import registry
from invenio_oarepo_oai_pmh_harvester.exceptions import ParserNotFoundError, HandlerNotFoundError, \
    NoMigrationError
from invenio_oarepo_oai_pmh_harvester.models import (OAIProvider, OAIRecord, OAIRecordExc)
from invenio_oarepo_oai_pmh_harvester.oai_base import OAIDBBase
from invenio_oarepo_oai_pmh_harvester.transformer import OAITransformer

oai_logger = logging.getLogger(__name__)
oai_logger.setLevel(logging.DEBUG)


class OAISynchronizer(OAIDBBase):
    """

    """

    def __init__(
            self,
            provider: OAIProvider,
            parser_name: str = None,
            unhandled_paths: set = None,
            validation: Callable = None,
            create_record: Callable = None,
            delete_record: Callable = None,
            update_record: Callable = None,
            pid_type: str = None,
            oai_identifiers: List[str] = None
    ):
        super().__init__(provider)
        self.pid_type = pid_type
        self.provider = provider
        self.oai_sync = None
        self.sickle = Sickle(self.provider.oai_endpoint)
        registry.load()
        self.parsers = provider.get_parsers()
        self.rules = provider.get_rules(parser_name) or {}
        self.parser = self.parsers.get(parser_name) or {}
        self.transformer = OAITransformer(self.rules, unhandled_paths=unhandled_paths)
        self.validation_handler = validation
        self.create_record_handler = create_record
        self.update_record_handler = update_record
        self.delete_record_handler = delete_record
        self.oai_identifiers = oai_identifiers

    def run(self, start_oai: str = None, start_id: int = None, break_on_error: bool = True):
        """

        :return:
        :rtype:
        """
        self.ensure_migration()
        super().run(start_oai=start_oai, start_id=start_id, break_on_error=break_on_error)

    def synchronize(self,
                    identifiers=None,
                    start_oai: str = None,
                    start_id: int = None,
                    break_on_error: bool = True):
        """

        :return:
        :rtype:
        """
        oai_logger.info(f"OAI harvester on endpoint: {self.provider.oai_endpoint} has started!")

        if identifiers is None:
            if self.oai_identifiers is None:
                identifiers = self._get_oai_identifiers()
            else:
                identifiers = self._get_oai_identifiers(identifiers_list=self.oai_identifiers)

        identifiers = islice(identifiers, start_id, None)
        collect = False
        for idx, identifier in enumerate(identifiers, start=start_id):
            oai_logger.info(f"{idx}. Record, OAI ID: '{identifier}'")
            datestamp = identifier.datestamp
            oai_identifier = identifier.identifier
            if not start_oai or oai_identifier == start_oai:
                collect = True
            if not collect:
                continue
            deleted = identifier.deleted
            try:
                if deleted:
                    self._delete(identifier, oai_identifier)
                else:
                    try:
                        self.update(oai_identifier, datestamp)
                    except IdDoesNotExist:
                        self._delete(identifier, oai_identifier)
                if idx % 100:
                    db.session.commit()
            except Exception:
                exc = traceback.format_exc()
                print(exc, "\n\n\n")
                oai_exc = OAIRecordExc.query.filter_by(oai_identifier=oai_identifier,
                                                       oai_sync_id=self.oai_sync.id).one_or_none()
                if not oai_exc:
                    oai_exc = OAIRecordExc(oai_identifier=oai_identifier, traceback=exc,
                                           oai_sync_id=self.oai_sync.id)
                    db.session.add(oai_exc)
                else:
                    oai_exc.traceback = exc
                db.session.commit()
                if break_on_error:
                    raise
                continue

    def _delete(self, identifier, oai_identifier):
        self.delete(oai_identifier)
        self.deleted += 1
        oai_logger.info(f"Identifier '{identifier}' has been marked as deleted")

    def _get_oai_identifiers(
            self,
            sickle=None,
            metadata_prefix=None,
            set_=None,
            identifiers_list: List[str] = None):
        if identifiers_list:
            return [self.sickle.GetRecord(identifier=identifier,
                                          metadataPrefix=self.provider.metadata_prefix).header for
                    identifier in identifiers_list]
        if not sickle:
            sickle = self.sickle
        if not metadata_prefix:
            metadata_prefix = self.provider.metadata_prefix
        if not set_:
            set_ = self.provider.set_
        return sickle.ListIdentifiers(metadataPrefix=metadata_prefix,
                                      set=set_)

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
        if oai_rec:
            our_datestamp = pytz.UTC.localize(oai_rec.timestamp)
            oai_record_datestamp = isoparse(datestamp)
            if our_datestamp >= oai_record_datestamp:
                return
        xml = self.get_xml(oai_identifier)
        parsed = self.parse(xml)
        transformed = self.transform(parsed)
        transformed.update(self.provider.constant_fields)
        if self.validation_handler:
            self.validation_handler(transformed)

        if oai_rec is None:
            transformed = self.attach_id(transformed)
            record = self.create_record(transformed)
            oai_rec = OAIRecord(
                id=record.id,
                oai_identifier=oai_identifier,
                creation_sync_id=self.oai_sync.id,
                nusl_id=transformed["id"]
            )
            self.created += 1
            db.session.add(oai_rec)
            oai_logger.info(
                f"Identifier '{oai_identifier}' has been created and '{record.id}' has been "
                f"assigned as a UUID")
        else:
            transformed = self.attach_id(transformed, nusl_id=oai_rec.nusl_id)
            record = self.update_record(transformed)
            self.modified += 1
            oai_rec.modification_sync_id = self.oai_sync.id
            oai_logger.info(f"Identifier '{oai_identifier}' has been updated (UUID: {record.id})")
        oai_rec.last_sync_id = self.oai_sync.id
        oai_rec.timestamp = datestamp
        oai_logger.debug(f"RECORD BEFORE INDEX: {record}")
        nusl_theses.index_draft_record(record)

    def transform(self, parsed, handler=None):
        if not handler:
            handler = self.transformer.transform
        return handler(parsed)

    def get_xml(self, oai_identifier):
        original_record = self.sickle.GetRecord(identifier=oai_identifier,
                                                metadataPrefix=self.provider.metadata_prefix)
        return original_record.xml

    def parse(self, xml_etree, parser=None):
        if not parser or not callable(parser):
            if self.parser:
                parser = self.parser
            if parser is None:
                raise ParserNotFoundError(
                    "No parser specified, please check entry points and parser designation by "
                    "decorator @Decorators.parser or specify parser as function parameter.")
        return parser(xml_etree)

    def create_record(self, metadata):
        """

        :return:
        :rtype:
        """
        if self.create_record_handler:
            record = self.create_record_handler(metadata, pid_type=self.pid_type)
            return record
        else:
            raise HandlerNotFoundError(
                'Please specify create handler during initialization. Must specify '
                '"create_record" named parameter')

    def update_record(self, metadata):
        """


        :return:
        :rtype:
        """
        if self.update_record_handler:
            existing_record = nusl_theses.get_record_by_id(self.pid_type, metadata["id"])
            return self.update_record_handler(existing_record, metadata)
        else:
            raise HandlerNotFoundError(
                'Please specify update handler during initialization. Must specify '
                '"update_record" named parameter')

    def delete(self, oai_identifier):
        """

        :param oai_identifier:
        :type oai_identifier:
        :return:
        :rtype:
        """
        if self.delete_record_handler:
            oai_record = OAIRecord.query.filter_by(oai_identifier=oai_identifier).one_or_none()
            if not oai_record:
                return
            record = nusl_theses.get_record_by_id(pid_type=self.pid_type,
                                                  pid_value=oai_record.nusl_id)
            self.delete_record_handler(record)
        else:
            raise HandlerNotFoundError(
                'Please specify delete handler during initialization. Must specify '
                '"delete_record" named parameter')

    @staticmethod
    def ensure_migration():
        # TODO: Zlepšit kontrolu zda proběhla migrace úspěšně
        oai_record_count = OAIRecord.query.count()
        records_count = RecordMetadata.query.count()
        if records_count > 0 and oai_record_count == 0:
            raise NoMigrationError(
                "There are records presents in database, but no OAIRecord found. Please ensure "
                "that you run migration script")

    @staticmethod
    def attach_id(transformed, nusl_id=None):
        if not nusl_id:
            nusl_id = str(nusl_theses.get_new_pid())
        transformed["id"] = nusl_id
        transformed["identifier"].append({
            "type": "nusl",
            "value": nusl_id
        })
        return transformed

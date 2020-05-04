import logging
from typing import Callable

from invenio_db import db
from invenio_records.models import RecordMetadata
from sickle import Sickle

from invenio_oarepo_oai_pmh_harvester import registry
from invenio_oarepo_oai_pmh_harvester.exceptions import ParserNotFoundError, HandlerNotFoundError, \
    NoMigrationError
from invenio_oarepo_oai_pmh_harvester.models import (OAIProvider, OAIRecord)
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
            update_record: Callable = None):
        super().__init__(provider)
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

    def run(self):
        """

        :return:
        :rtype:
        """
        self.ensure_migration()
        super().run()

    def synchronize(self, identifiers=None):
        """

        :return:
        :rtype:
        """
        oai_logger.info(f"OAI harvester on endpoint: {self.provider.oai_endpoint} has started!")

        if identifiers is None:
            identifiers = self._get_oai_identifiers()

        for identifier in identifiers:
            datestamp = identifier.datestamp
            oai_identifier = identifier.identifier
            deleted = identifier.deleted
            with db.session.begin_nested():
                if deleted:
                    self.delete(oai_identifier, datestamp)
                    self.deleted += 1
                else:
                    self.update(oai_identifier, datestamp)

    def _get_oai_identifiers(
            self,
            sickle=None,
            metadata_prefix=None,
            set_=None):
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
        original_record = self.sickle.GetRecord(identifier=oai_identifier,
                                                metadataPrefix=self.provider.metadata_prefix)

        parsed = self.parse(original_record.xml)
        transformed = self.transformer.transform(parsed)
        transformed.update(self.provider.constant_fields)
        if self.validation_handler:
            self.validation_handler(transformed)

        # sem přijdou metadata
        if oai_rec is None:
            record_id = self.create_record(transformed, oai_identifier)
            oai_rec = OAIRecord(id=record_id, oai_identifier=oai_identifier,
                                creation_sync_id=self.oai_sync.id)
            self.created += 1
        else:
            self.update_record(transformed, oai_identifier)
            self.modified += 1
            oai_rec.modification_sync_id = self.oai_sync.id
        oai_rec.last_sync_id = self.oai_sync.id
        oai_rec.timestamp = datestamp
        db.session.add(oai_rec)
        db.session.commit()

    def parse(self, xml_etree, parser=None):
        if not parser or not callable(parser):
            if self.parser:
                parser = self.parser
            if parser is None:
                raise ParserNotFoundError(
                    "No parser specified, please check entry points and parser designation by "
                    "decorator @Decorators.parser or specify parser as function parameter.")
        return parser(xml_etree)

    def create_record(self, metadata, oai_identifier):
        """

        :param oai_identifier:
        :type oai_identifier:
        :return:
        :rtype:
        """
        if self.create_record_handler:
            record_id = self.create_record_handler(metadata, oai_identifier)
            return record_id
        else:
            raise HandlerNotFoundError(
                'Please specify create handler during initialization. Must specify '
                '"create_record" named parameter')

    def update_record(self, metadata, oai_identifier):
        """

        :param oai_identifier:
        :type oai_identifier:
        :return:
        :rtype:
        """
        if self.update_record_handler:
            self.update_record_handler(metadata, oai_identifier)
        else:
            raise HandlerNotFoundError(
                'Please specify update handler during initialization. Must specify '
                '"update_record" named parameter')

    def delete(self, oai_identifier, datestamp):
        """

        :param oai_identifier:
        :type oai_identifier:
        :param datestamp:
        :type datestamp:
        :return:
        :rtype:
        """
        if self.delete_record_handler:
            self.delete_record_handler(oai_identifier, datestamp)
        else:
            raise HandlerNotFoundError(
                'Please specify delete handler during initialization. Must specify '
                '"delete_record" named parameter')

    def ensure_migration(self):
        # TODO: Zlepšit kontrolu zda proběhla migrace úspěšně
        oai_record_count = OAIRecord.query.count()
        records_count = RecordMetadata.query.count()
        if records_count > 0 and oai_record_count == 0:
            raise NoMigrationError(
                "There are records presents in database, but no OAIRecord found. Please ensure "
                "that you run migration script")

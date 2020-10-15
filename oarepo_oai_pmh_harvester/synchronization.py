import logging
import traceback
import uuid
from itertools import islice
from typing import Callable, List

import pytz
from dateutil.parser import isoparse
from invenio_db import db
from invenio_pidstore import current_pidstore
from invenio_pidstore.models import PersistentIdentifier
from invenio_records import Record
from invenio_records_rest.utils import obj_or_import_string
from sickle import Sickle
from sickle.oaiexceptions import IdDoesNotExist

from oarepo_oai_pmh_harvester.exceptions import ParserNotFoundError
from oarepo_oai_pmh_harvester.models import (OAIProvider, OAIRecord, OAIRecordExc)
from oarepo_oai_pmh_harvester.oai_base import OAIDBBase

oai_logger = logging.getLogger(__name__)
oai_logger.setLevel(logging.DEBUG)


# TODO: převést pod providera
class OAISynchronizer(OAIDBBase):
    """

    """

    def __init__(
            self,
            provider: OAIProvider,
            parser: Callable = None,
            transformer=None,
            oai_identifiers: List[str] = None,
            endpoints=None,
            default_endpoint: str = "recid",
            endpoint_mapping=None
    ):
        super().__init__(provider)
        if endpoint_mapping is None:
            endpoint_mapping = {}
        self.provider = provider
        self.oai_sync = None
        self.sickle = Sickle(self.provider.oai_endpoint)
        self.parser = parser
        self.transformer = transformer
        self.oai_identifiers = oai_identifiers
        self.endpoints = endpoints
        self.default_endpoint = default_endpoint
        self.endpoint_mapping = endpoint_mapping

    def run(self, start_oai: str = None, start_id: int = 0, break_on_error: bool = True):
        """

        :return:
        :rtype:
        """
        # self.ensure_migration() TODO: dovyřešit
        super().run(start_oai=start_oai, start_id=start_id, break_on_error=break_on_error)

    def synchronize(self,
                    identifiers=None,
                    start_oai: str = None,
                    start_id: int = 0,
                    break_on_error: bool = True):
        """

        :return:
        :rtype:
        """
        oai_logger.info(f"OAI harvester on endpoint: {self.provider.oai_endpoint} has started!")

        identifiers = self._get_identifiers(identifiers, start_id)
        collect = False
        for idx, identifier in enumerate(identifiers, start=start_id):
            oai_logger.info(f"{idx}. Record, OAI ID: '{identifier}'")
            datestamp = identifier.datestamp
            oai_identifier = identifier.identifier
            if not start_oai or oai_identifier == start_oai:
                collect = True
            if not collect:  # pragma: no cover
                continue
            deleted = identifier.deleted
            try:
                if deleted:
                    self._delete(identifier, oai_identifier)
                else:
                    try:
                        self.create_or_update(oai_identifier, datestamp)
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

    def _get_identifiers(self, identifiers=None, start_id: int = 0):
        if identifiers is None:
            if self.oai_identifiers is None:
                identifiers = self._get_oai_identifiers()
            else:
                identifiers = self._get_oai_identifiers(identifiers_list=self.oai_identifiers)
        identifiers = islice(identifiers, start_id, None)
        return identifiers

    def _delete(self, identifier, oai_identifier):
        # TODO: přepsat, aby byla správně volána metoda delete_record
        self.delete_record(oai_identifier)
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

    def create_or_update(self, oai_identifier, datestamp):
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
                oai_logger.info(f'Record with oai_identifier "{oai_identifier}" already exists')
                return
        xml = self.get_xml(oai_identifier)
        parsed = self.parse(xml)
        transformed = self.transform(parsed)
        transformed.update(self.provider.constant_fields)

        if oai_rec is None:
            record = self.create_record(transformed)
            oai_rec = OAIRecord(
                id=record.id,
                oai_identifier=oai_identifier,
                creation_sync_id=self.oai_sync.id,
                pid=transformed["id"]
            )
            self.created += 1
            db.session.add(oai_rec)
            oai_logger.info(
                f"Identifier '{oai_identifier}' has been created and '{record.id}' has been "
                f"assigned as a UUID")
        else:
            record = self.update_record(oai_rec, transformed)
            self.modified += 1
            oai_rec.modification_sync_id = self.oai_sync.id
            oai_logger.info(f"Identifier '{oai_identifier}' has been updated (UUID: {record.id})")
        oai_rec.last_sync_id = self.oai_sync.id
        oai_rec.timestamp = datestamp
        return record

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

    def create_record(self, data):
        minter = self.get_minter()
        record_class = self.get_record_class()
        indexer_class = self.get_indexer_class()

        # Create uuid for record
        record_uuid = uuid.uuid4()
        # Create persistent identifier
        pid = minter(record_uuid, data=data)
        # Create record
        record = record_class.create(data, id_=record_uuid)

        db.session.commit()

        # Index the record
        if indexer_class:
            indexer_class().index(record)

        return record

    def update_record(self, oai_rec, data):
        indexer_class = self.get_indexer_class()

        record = Record.get_record(oai_rec.id)
        record.clear()
        record.update(data)
        record.commit()
        db.session.commit()
        if indexer_class:
            indexer_class().index(record)
        return record

    def delete_record(self, oai_rec):
        indexer_class = self.get_indexer_class()

        record = Record.get_record(oai_rec.id)
        record.delete()
        # mark all PIDs as DELETED
        all_pids = PersistentIdentifier.query.filter(
            PersistentIdentifier.object_uuid == record.id,
        ).all()
        for rec_pid in all_pids:
            if not rec_pid.is_deleted():
                rec_pid.delete()
        db.session.commit()
        if indexer_class:
            indexer_class().delete(record)

    @staticmethod
    def ensure_migration():
        # TODO: Zlepšit kontrolu zda proběhla migrace úspěšně
        pass
        # oai_record_count = OAIRecord.query.count()
        # records_count = RecordMetadata.query.count()
        # if records_count > 0 and oai_record_count == 0:
        #     raise NoMigrationError(
        #         "There are records presents in database, but no OAIRecord found. Please ensure "
        #         "that you run migration script")

    def get_endpoint_config(self, data):
        end_point_name = None
        if not data:
            data = {}
        if self.endpoint_mapping:
            end_point_name = self.endpoint_mapping["mapping"].get(
                data.get(self.endpoint_mapping["field_name"]))
        endpoint_config = self.endpoints.get(end_point_name) or self.endpoints.get(
            self.default_endpoint)
        return endpoint_config

    def get_minter(self, data=None):
        endpoint_config = self.get_endpoint_config(data)
        minter_name = endpoint_config["pid_minter"]
        return current_pidstore.minters.get(minter_name)

    def get_record_class(self, data=None):
        endpoint_config = self.get_endpoint_config(data)
        record_class = endpoint_config["record_class"]
        return obj_or_import_string(record_class)

    def get_indexer_class(self, data=None):
        endpoint_config = self.get_endpoint_config(data)
        record_class = endpoint_config["indexer_class"]
        return obj_or_import_string(record_class)

import datetime
import logging
import traceback
import uuid
from itertools import islice
from typing import Callable, List

import pytz
from dateutil.parser import isoparse
from flask import current_app
from invenio_db import db
from invenio_pidstore import current_pidstore
from invenio_pidstore.models import PersistentIdentifier
from invenio_records import Record
from invenio_records_rest.utils import obj_or_import_string
from lxml.etree import _Element
from sickle import Sickle
from sickle.models import Header
from sickle.oaiexceptions import IdDoesNotExist

from oarepo_oai_pmh_harvester.exceptions import ParserNotFoundError
from oarepo_oai_pmh_harvester.models import (OAIProvider, OAIRecord, OAIRecordExc, OAISync)

oai_logger = logging.getLogger(__name__)
oai_logger.setLevel(logging.DEBUG)


# TODO: převést pod providera
class OAISynchronizer:
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
            endpoint_mapping=None,
            pid_field=None
    ):
        self.provider = provider

        # Counters
        self.deleted = 0
        self.created = 0
        self.modified = 0

        if endpoint_mapping is None:
            endpoint_mapping = {}
        if pid_field is None:
            self.pid_field = current_app.config.get('PIDSTORE_RECID_FIELD', "recid")
        else:
            self.pid_field = pid_field
        self.provider = provider
        self.oai_sync = None
        self.sickle = Sickle(self.provider.oai_endpoint)
        self.parser = parser
        self.transformer = transformer
        self.oai_identifiers = oai_identifiers
        self.endpoints = endpoints
        self.default_endpoint = default_endpoint
        self.endpoint_mapping = endpoint_mapping

    def run(self, start_oai: str = None, start_id: int = None, break_on_error: bool = True):
        """

        :return:
        :rtype:
        """
        self.restart_counters()
        with db.session.begin_nested():
            self.oai_sync = OAISync(
                provider=self.provider,
                sync_start=datetime.datetime.utcnow(),
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
            self.oai_sync.sync_end = datetime.datetime.utcnow()
            self.oai_sync.rec_modified = self.modified
            self.oai_sync.rec_created = self.created
            self.oai_sync.rec_deleted = self.deleted
            if status == "failed":
                self.oai_sync.logs = traceback.format_exc()
            db.session.add(self.oai_sync)
        db.session.commit()

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
        for idx, identifier in enumerate(identifiers, start=start_id):
            oai_logger.info(f"{idx}. Record, OAI ID: '{identifier}'")
            datestamp, deleted, oai_identifier = self.get_oai_header_data(identifier)
            oai_rec = OAIRecord.get_record(oai_identifier)
            if not start_oai or oai_identifier == start_oai:  # pragma: no cover
                collect = True
            else:
                collect = False
            if not collect:  # pragma: no cover
                continue
            try:
                self.record_crud(oai_rec, datestamp=datestamp, deleted=deleted, idx=idx, oai_identifier=oai_identifier,)
            except Exception:
                self.exception_handler(oai_identifier)
                if break_on_error:
                    raise
                continue

    def exception_handler(self, oai_identifier):
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

    def record_crud(self,
                    oai_rec: OAIRecord = None,
                    oai_identifier: str = None,
                    datestamp: str = datetime.datetime.utcnow().isoformat(),
                    deleted: bool = False,
                    xml: _Element = None,
                    idx: int = 0):
        if not (oai_rec or oai_identifier):
            raise Exception("You have to provide oai_rec or oai_identifier")
        if not oai_identifier:
            oai_identifier = oai_rec.oai_identifier
        if deleted:
            self._delete(oai_rec)
        else:
            try:
                self.create_or_update(oai_identifier, datestamp, oai_rec=oai_rec, xml=xml)
            except IdDoesNotExist:
                self._delete(oai_rec)
        if idx % 100:
            db.session.commit()

    def get_oai_header_data(self, identifier: Header):
        datestamp = identifier.datestamp
        oai_identifier = identifier.identifier
        deleted = identifier.deleted
        return datestamp, deleted, oai_identifier

    def _get_identifiers(self, identifiers=None, start_id: int = 0):
        if identifiers is None:
            if self.oai_identifiers is None:
                identifiers = self._get_oai_identifiers()
            else:
                identifiers = self._get_oai_identifiers(identifiers_list=self.oai_identifiers)
        identifiers = islice(identifiers, start_id, None)
        return identifiers

    def _delete(self, oai_rec):
        self.delete_record(oai_rec)
        self.deleted += 1
        oai_logger.info(f"Identifier '{oai_rec.oai_identifier}' has been marked as deleted")

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

    def create_or_update(self, oai_identifier, datestamp, oai_rec=None, xml: _Element = None):
        if oai_rec:
            our_datestamp = pytz.UTC.localize(oai_rec.timestamp)
            oai_record_datestamp = isoparse(datestamp)
            if our_datestamp >= oai_record_datestamp:
                oai_logger.info(f'Record with oai_identifier "{oai_identifier}" already exists')
                return
        if not xml:
            xml = self.get_xml(oai_identifier)
        parsed = self.parse(xml)
        transformed = self.transform(parsed)
        transformed.update(self.provider.constant_fields)

        if oai_rec is None:
            record, pid = self.create_record(transformed)
            oai_rec = OAIRecord(
                id=record.id,
                oai_identifier=oai_identifier,
                creation_sync_id=self.oai_sync.id,
                pid=pid.pid_value  # TODO: tady musí být fetcher
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
        oai_rec.timestamp = isoparse(datestamp)
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

        return record, pid

    def update_record(self, oai_rec, data):
        indexer_class = self.get_indexer_class()
        fetcher = self.get_fetcher(data)
        record = Record.get_record(oai_rec.id)
        pid = fetcher(oai_rec.id, dict(record))
        record.clear()
        record.update(data)
        record[self.pid_field] = pid.pid_value
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

    def get_fetcher(self, data=None):
        endpoint_config = self.get_endpoint_config(data)
        fetcher_name = endpoint_config["pid_fetcher"]
        return current_pidstore.fetchers.get(fetcher_name)

    def get_record_class(self, data=None):
        endpoint_config = self.get_endpoint_config(data)
        record_class = endpoint_config["record_class"]
        return obj_or_import_string(record_class)

    def get_indexer_class(self, data=None):
        endpoint_config = self.get_endpoint_config(data)
        record_class = endpoint_config["indexer_class"]
        return obj_or_import_string(record_class)

    def restart_counters(self):
        self.deleted = 0
        self.created = 0
        self.modified = 0

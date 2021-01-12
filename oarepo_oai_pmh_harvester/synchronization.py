import traceback
import uuid
from itertools import islice
from typing import Callable, List, Union

import arrow
import time
from flask import current_app
from invenio_db import db
from invenio_pidstore import current_pidstore
from invenio_records import Record
from invenio_records_rest.utils import obj_or_import_string
from lxml.etree import _Element
from requests import HTTPError
from sickle import Sickle
from sickle.models import Header
from sickle.oaiexceptions import IdDoesNotExist
from sqlalchemy.orm.exc import NoResultFound

from oarepo_oai_pmh_harvester.exceptions import ParserNotFoundError
from oarepo_oai_pmh_harvester.models import (OAIRecord, OAIRecordExc, OAISync)
from oarepo_oai_pmh_harvester.utils import get_oai_header_data


class OAISynchronizer:
    """

    """

    def __init__(
            self,
            name,
            provider_code,
            oai_endpoint,
            metadata_prefix,
            set_,
            constant_fields: dict = None,
            parser: Callable = None,
            transformer=None,
            endpoints=None,
            default_endpoint: str = "recid",
            endpoint_mapping=None,
            pid_field=None,
            from_: str = None,
            endpoint_handler: dict = None,
            bulk: bool = True,
            pre_processors: dict = None,
            post_processors: dict = None
    ):

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
        self.name = name
        self.provider_code = provider_code
        self.metadata_prefix = metadata_prefix
        self.oai_endpoint = oai_endpoint
        self.oai_sync = None
        self.sickle = Sickle(self.oai_endpoint)
        self.parser = parser
        self.transformer = transformer
        self.endpoints = endpoints
        self.default_endpoint = default_endpoint
        self.endpoint_mapping = endpoint_mapping
        self.set_ = set_
        if constant_fields:
            self.constant_fields = constant_fields
        else:
            self.constant_fields = {}
        self._from = None
        if from_:
            self.from_ = from_
        self.endpoint_handler = endpoint_handler
        self.bulk = bulk
        self.pre_processors = pre_processors
        self.post_processors = post_processors
        self.overwrite = False

    @property
    def from_(self):
        return self._from

    @from_.setter
    def from_(self, value):
        if value == "latest":
            last_sync = OAISync.query.order_by(OAISync.id.desc()).first()
            if last_sync:
                self._from = arrow.get(last_sync)
        elif value is not None:
            if isinstance(value, arrow.Arrow):
                self._from = value
            else:
                self._from = arrow.get(value)
        else:
            self._from = None

    def run(self, start_oai: str = None, start_id: int = 0, break_on_error: bool = True,
            oai_id: Union[str, List[str]] = None, overwrite: bool = False):
        """

        :return:
        :rtype:
        """
        self.overwrite = overwrite
        self.restart_counters()
        with db.session.begin_nested():
            self.oai_sync = OAISync(
                provider_code=self.provider_code,  # TODO: nahradit provider.code
                synchronizer_code=self.name,
                sync_start=arrow.utcnow().datetime,  # datetime.datetime.utcnow(),
                status="active")
            db.session.add(self.oai_sync)
        db.session.commit()
        try:
            if oai_id:
                if isinstance(oai_id, str):
                    oai_ids = [oai_id]
                elif isinstance(oai_id, list):
                    oai_ids = oai_id
                else:
                    raise Exception("OAI identifier must be string or list of strings")
                self.synchronize(identifiers=oai_ids, break_on_error=break_on_error)
                self.update_oai_sync("ok")
            else:
                self.synchronize(start_oai=start_oai, start_id=start_id,
                                 break_on_error=break_on_error)
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
            self.oai_sync.sync_end = arrow.utcnow().datetime  # datetime.datetime.utcnow()
            self.oai_sync.records_modified = self.modified
            self.oai_sync.records_created = self.created
            self.oai_sync.records_deleted = self.deleted
            if status == "failed":
                self.oai_sync.logs = traceback.format_exc()
            db.session.add(self.oai_sync)
        db.session.commit()

    def synchronize(self,
                    identifiers=None,
                    start_oai: str = None,
                    start_id: int = 0,
                    break_on_error: bool = True):  # pragma: no cover
        """

        :return:
        :rtype:
        """
        print(f"OAI harvester on endpoint: {self.oai_endpoint} has started!")

        if not self.bulk:
            identifiers = self._get_identifiers(identifiers, start_id)
            for idx, identifier in enumerate(identifiers, start=start_id):
                self.record_handling(idx, start_oai, break_on_error, identifier)
        else:
            records = self._get_records_iterator(start_id, list_identifiers=identifiers)
            print("Waiting for server...")
            for idx, record in enumerate(records, start=start_id):
                self.record_handling(idx, start_oai, break_on_error, xml=record.xml)

    def _get_records_iterator(self, start_id: int = 0, list_identifiers: List[str] = None):
        if self.from_:
            records = self.sickle.ListRecords(
                **{
                    "metadataPrefix": self.metadata_prefix,
                    "set": self.set_,
                    "from": self.from_.format("YYYY-MM-DD")
                }
            )
        else:
            records = self.sickle.ListRecords(metadataPrefix=self.metadata_prefix, set=self.set_)
        if list_identifiers:
            return self.record_filter_generator(records, list_identifiers)
        else:
            return islice(records, start_id, None)

    def record_filter_generator(self, iterator, identifiers_list):
        for record in iterator:
            if record.header.identifier in identifiers_list:
                yield record

    def record_handling(self, idx, start_oai: str = None, break_on_error: bool = True,
                        identifier: Header = None,
                        xml: _Element = None):
        if not (identifier or xml):
            raise Exception("Must provide header or xml")
        if identifier and xml:
            raise Exception("You must provide only header or xml")
        if identifier:
            datestamp, deleted, oai_identifier = get_oai_header_data(identifier)
        else:
            datestamp, deleted, oai_identifier = get_oai_header_data(xml=xml)
        print(f"{idx}. Record, OAI ID: '{oai_identifier}'")
        oai_rec = OAIRecord.get_record(oai_identifier)
        if not start_oai or oai_identifier == start_oai:  # pragma: no cover TODO: vyřešit
            # start_oai/není implemntováno
            collect = True
        else:
            collect = False
        if not collect:  # pragma: no cover
            return
        try:
            self.record_crud(oai_rec, timestamp=datestamp, deleted=deleted, idx=idx,
                             oai_identifier=oai_identifier, xml=xml)
        except Exception:  # pragma: no cover
            self.exception_handler(oai_identifier)
            if break_on_error:
                raise
            return

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
                    timestamp: str = arrow.utcnow().isoformat(),
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
                self.create_or_update(oai_identifier, timestamp, oai_rec=oai_rec, xml=xml)
            except IdDoesNotExist:  # pragma: no cover
                self._delete(oai_rec)
        if idx % 100:
            db.session.commit()

    def _get_identifiers(self, identifiers=None, start_id: int = 0):
        if identifiers is None:
            identifiers = self._get_oai_identifiers()
        else:
            identifiers = self._get_oai_identifiers(identifiers_list=identifiers)
        identifiers = islice(identifiers, start_id, None)
        return identifiers

    def _delete(self, oai_rec):
        if not oai_rec:
            return
        self.delete_record(oai_rec)
        self.deleted += 1
        print(f"Identifier '{oai_rec.oai_identifier}' has been marked as deleted")

    def _get_oai_identifiers(
            self,
            sickle=None,
            metadata_prefix=None,
            set_=None,
            identifiers_list: List[str] = None,
            from_: arrow.Arrow = None
    ):
        if identifiers_list:
            return [self.sickle.GetRecord(identifier=identifier,
                                          metadataPrefix=self.metadata_prefix).header for
                    identifier in identifiers_list]
        if not sickle:
            sickle = self.sickle
        if not metadata_prefix:
            metadata_prefix = self.metadata_prefix
        if not set_:
            set_ = self.set_
        if not from_:
            if self.from_:
                from_ = self.from_
            else:
                return sickle.ListIdentifiers(metadataPrefix=metadata_prefix,
                                              set=set_)
        return sickle.ListIdentifiers(
            **{
                "metadataPrefix": metadata_prefix,
                "set": set_,
                "from": from_.format("YYYY-MM-DD")
            }
        )

    def create_or_update(self, oai_identifier, datestamp: str, oai_rec=None, xml: _Element = None):
        if oai_rec:
            if not self.overwrite:
                our_datestamp = arrow.get(oai_rec.timestamp)
                oai_record_datestamp = arrow.get(datestamp)
                if our_datestamp >= oai_record_datestamp:
                    print(f'Record with oai_identifier "{oai_identifier}" already exists')
                    return
        if not xml:
            xml = self.get_xml(oai_identifier)
        parsed = self.parse(xml)
        if self.pre_processors:
            for processor in self.pre_processors:
                parsed = processor(parsed)
        transformed = self.transform(parsed)
        if self.post_processors:
            for processor in self.post_processors:
                transformed = processor(transformed)
        transformed.update(self.constant_fields)

        if oai_rec is None:
            record, pid = self.create_record(transformed)
            oai_rec = OAIRecord(
                id=record.id,
                oai_identifier=oai_identifier,
                creation_sync_id=self.oai_sync.id,
                pid=pid.pid_value
            )
            self.created += 1
            db.session.add(oai_rec)
            print(
                f"Identifier '{oai_identifier}' has been created and '{record.id}' has been "
                f"assigned as a UUID")
        else:
            record = self.update_record(oai_rec, transformed)
            self.modified += 1
            oai_rec.modification_sync_id = self.oai_sync.id
            print(f"Identifier '{oai_identifier}' has been updated (UUID: {record.id})")
        oai_rec.last_sync_id = self.oai_sync.id
        oai_rec.timestamp = arrow.get(datestamp).datetime
        return record

    def transform(self, parsed, handler=None):
        if not handler:
            handler = self.transformer.transform
        return handler(parsed)

    def get_xml(self, oai_identifier, retry=True):
        try:
            original_record = self.sickle.GetRecord(identifier=oai_identifier,
                                                metadataPrefix=self.metadata_prefix)
        except HTTPError:
            if retry:
                time.sleep(1)
                original_record = self.sickle.GetRecord(identifier=oai_identifier,
                                                        metadataPrefix=self.metadata_prefix)
            else:
                raise

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
        endpoint_config = self.get_endpoint_config(data)
        minter = self.get_minter(data, endpoint_config=endpoint_config)
        record_class = self.get_record_class(data, endpoint_config=endpoint_config)
        indexer_class = self.get_indexer_class(data, endpoint_config=endpoint_config)

        # Create uuid for record
        record_uuid = uuid.uuid4()
        # Create persistent identifier
        pid = minter(record_uuid, data=data)
        # Create record
        try:
            record = record_class.create(data, id_=pid.object_uuid)
        except:
            db.session.rollback()
            raise
        else:
            db.session.commit()

        # Index the record
        if indexer_class:
            indexer_class().index(record)

        return record, pid

    def update_record(self, oai_rec, data):
        endpoint_config = self.get_endpoint_config(data)
        indexer_class = self.get_indexer_class(data, endpoint_config=endpoint_config)
        record_class = self.get_record_class(data, endpoint_config=endpoint_config)
        fetcher = self.get_fetcher(data)
        try:
            record = record_class.get_record(oai_rec.id)
        except NoResultFound:
            record = record_class.get_record(oai_rec.id, with_deleted=True)
            record.revert(-2)
            record.update(record.model.json)
        fetched_pid = fetcher(oai_rec.id, dict(record))
        record.clear()
        record.update(data)
        record[self.pid_field] = fetched_pid.pid_value
        record.commit()
        db.session.commit()
        if indexer_class:
            indexer_class().index(record)
        return record

    def delete_record(self, oai_rec):
        if not oai_rec:
            return
        indexer_class = self.get_indexer_class()

        record = Record.get_record(oai_rec.id)
        record.delete()
        # TODO: rozmyslet se jak nakládat s PIDy
        # # mark all PIDs as DELETED
        # all_pids = PersistentIdentifier.query.filter(
        #     PersistentIdentifier.object_uuid == record.id,
        # ).all()
        # for rec_pid in all_pids:
        #     if not rec_pid.is_deleted():
        #         rec_pid.delete()

        db.session.commit()
        if indexer_class:
            indexer_class().delete(record)

    def get_endpoint_config(self, data):
        endpoint_name = None
        if not data:
            data = {}
        if self.endpoint_mapping:
            endpoint_name = self.endpoint_mapping["mapping"].get(
                data.get(self.endpoint_mapping["field_name"]))
        if not endpoint_name and self.endpoint_handler:
            provider = self.endpoint_handler.get(self.provider_code)
            if provider:
                handler = provider.get(self.metadata_prefix)
                if handler:
                    endpoint_name = handler(data)
        draft_configs = current_app.config.get("RECORDS_DRAFT_ENDPOINTS")
        if draft_configs:
            draft_endpoint_config = draft_configs.get(endpoint_name)
            if draft_endpoint_config:
                draft_endpoint_name = draft_endpoint_config.get("draft")
                if draft_endpoint_name:
                    endpoint_name = draft_endpoint_name
        endpoint_config = self.endpoints.get(endpoint_name) or self.endpoints.get(
            self.default_endpoint)
        return endpoint_config

    def get_minter(self, data=None, endpoint_config=None):
        if not endpoint_config:
            endpoint_config = self.get_endpoint_config(data)
        minter_name = endpoint_config["pid_minter"]
        return current_pidstore.minters.get(minter_name)

    def get_fetcher(self, data=None, endpoint_config=None):
        if not endpoint_config:
            endpoint_config = self.get_endpoint_config(data)
        fetcher_name = endpoint_config["pid_fetcher"]
        return current_pidstore.fetchers.get(fetcher_name)

    def get_record_class(self, data=None, endpoint_config=None):
        if not endpoint_config:
            endpoint_config = self.get_endpoint_config(data)
        record_class = endpoint_config["record_class"]
        return obj_or_import_string(record_class)

    def get_indexer_class(self, data=None, endpoint_config=None):
        if not endpoint_config:
            endpoint_config = self.get_endpoint_config(data)
        indexer_class = endpoint_config.get("indexer_class", 'invenio_indexer.api.RecordIndexer')
        return obj_or_import_string(indexer_class)

    def restart_counters(self):
        self.deleted = 0
        self.created = 0
        self.modified = 0

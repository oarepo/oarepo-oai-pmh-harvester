from collections import defaultdict
from datetime import datetime
from itertools import islice
from pprint import pprint

import pytest
import requests
from invenio_records import Record
from lxml.etree import _Element
from pytest import skip
from pytz import utc
from sickle.iterator import OAIItemIterator
from sqlalchemy.orm.exc import NoResultFound

from oarepo_oai_pmh_harvester.models import OAIRecord, OAISync, OAIProvider
from oarepo_oai_pmh_harvester.proxies import current_oai_client


class TestSynchronization:
    def test_get_endpoint_config(self, load_entry_points, app, db, metadata):
        synchronizer = current_oai_client.synchronizers["uk"]
        res = synchronizer.get_endpoint_config(metadata)
        assert res is not None
        assert isinstance(res, dict)

    def test_create_record(self, load_entry_points, app, db, metadata, ):
        synchronizers = app.extensions['oarepo-oai-client'].synchronizers
        synchronizer = synchronizers["uk"]
        rec, pid = synchronizer.create_record(metadata)
        assert rec == {'title': 'Testovací záznam', 'pid': '1'}

    def test_update_record(self, load_entry_points, app, db, metadata):
        synchronizers = current_oai_client.synchronizers
        synchronizer = synchronizers["uk"]
        record, id_ = synchronizer.create_record(metadata)
        provider = OAIProvider.query.filter_by(code="uk").one_or_none()
        if not provider:
            current_oai_client.create_providers()
        oai_sync = OAISync(provider_id=1)
        db.session.add(oai_sync)
        db.session.commit()
        oai_rec = OAIRecord(
            id=record.id,
            oai_identifier="oai:example.cz:1",
            creation_sync_id=oai_sync.id,
            pid="1",
            timestamp=datetime.now()
        )
        db.session.add(oai_rec)
        db.session.commit()
        metadata["title"] = "Updated record"
        record2 = synchronizer.update_record(oai_rec, metadata)
        assert record2 == {'title': 'Updated record', 'pid': '1'}

    def test_delete_record(self, load_entry_points, app, db, metadata):
        synchronizers = current_oai_client.synchronizers
        synchronizer = synchronizers["uk"]
        provider = OAIProvider.query.filter_by(code="uk").one_or_none()
        if not provider:
            current_oai_client.create_providers()
        record, id_ = synchronizer.create_record(metadata)
        oai_sync = OAISync(provider_id=1)
        db.session.add(oai_sync)
        db.session.commit()
        oai_rec = OAIRecord(
            id=record.id,
            oai_identifier="oai:example.cz:1",
            creation_sync_id=oai_sync.id,
            pid="1",
            timestamp=datetime.now()
        )
        db.session.add(oai_rec)
        db.session.commit()
        synchronizer.delete_record(oai_rec)
        with pytest.raises(NoResultFound):
            Record.get_record(oai_rec.id)
        deleted_record = Record.get_record(oai_rec.id, with_deleted=True)

    def test_delete(self, load_entry_points, app, db, metadata):
        synchronizers = current_oai_client.synchronizers
        synchronizer = synchronizers["uk"]
        provider = OAIProvider.query.filter_by(code="uk").one_or_none()
        if not provider:
            current_oai_client.create_providers()
        record, id_ = synchronizer.create_record(metadata)
        oai_sync = OAISync(provider_id=1)
        db.session.add(oai_sync)
        db.session.commit()
        oai_rec = OAIRecord(
            id=record.id,
            oai_identifier="oai:example.cz:1",
            creation_sync_id=oai_sync.id,
            pid="1",
            timestamp=datetime.now()
        )
        db.session.add(oai_rec)
        db.session.commit()
        metadata["title"] = "Updated record"
        synchronizer._delete(oai_rec)
        with pytest.raises(NoResultFound):
            Record.get_record(oai_rec.id)
        deleted_record = Record.get_record(oai_rec.id, with_deleted=True)

    def test_get_xml(self, load_entry_points, app, db):
        synchronizers = current_oai_client.synchronizers
        synchronizer = synchronizers["uk"]
        try:
            xml = synchronizer.get_xml("oai:dspace.cuni.cz:20.500.11956/111006")
        except requests.exceptions.RequestException:
            skip("Connection failed")
        assert isinstance(xml, _Element)

    def test_parse(self, load_entry_points, app, db, record_xml, parsed_record_xml):
        def default_to_regular(d):
            if isinstance(d, defaultdict):
                d = {k: default_to_regular(v) for k, v in d.items()}
            if isinstance(d, (list, tuple)):
                d = [default_to_regular(_) for _ in d]
            return d

        synchronizers = current_oai_client.synchronizers
        synchronizer = synchronizers["uk"]
        parsed = synchronizer.parse(record_xml)
        res = default_to_regular(parsed)
        assert res == parsed_record_xml

    def test_get_oai_identifiers(self, load_entry_points, app, db):
        synchronizers = current_oai_client.synchronizers
        synchronizer = synchronizers["uk"]
        ids = synchronizer._get_oai_identifiers()
        assert isinstance(ids, OAIItemIterator)

    def test_get_oai_identifiers_2(self, load_entry_points, app, db):
        synchronizers = current_oai_client.synchronizers
        synchronizer = synchronizers["uk"]
        ids = synchronizer._get_oai_identifiers(
            identifiers_list=["oai:dspace.cuni.cz:20.500.11956/111006"])
        assert len(ids) == 1
        assert isinstance(ids, list)

    def test_get_identifiers(self, load_entry_points, app, db):
        synchronizers = current_oai_client.synchronizers
        synchronizer = synchronizers["uk"]
        ids = synchronizer._get_identifiers()
        assert isinstance(ids, islice)

    def test_transform(self, load_entry_points, app, db):
        synchronizers = current_oai_client.synchronizers
        synchronizer = synchronizers["uk"]
        transformed = synchronizer.transform({})
        assert transformed == {}

    def test_create_or_update(self, load_entry_points, app, db, record_xml):
        synchronizers = current_oai_client.synchronizers
        synchronizer = synchronizers["uk"]
        oai_sync = OAISync(provider_id=1)
        synchronizer.oai_sync = oai_sync
        record = synchronizer.create_or_update("oai:dspace.cuni.cz:20.500.11956/2623",
                                               '2017-09-11T08:12:53Z', xml=record_xml)
        db.session.commit()
        assert record == {'pid': '1', 'title': 'Testovací záznam'}
        oai_rec = OAIRecord.query.filter_by(pid=1).one_or_none()
        record2 = synchronizer.create_or_update("oai:dspace.cuni.cz:20.500.11956/2623",
                                                '2017-09-11T08:12:53Z', xml=record_xml,
                                                oai_rec=oai_rec)
        assert record2 is None
        new_time_stemp = datetime.utcnow().replace(tzinfo=utc).isoformat()
        record3 = synchronizer.create_or_update("oai:dspace.cuni.cz:20.500.11956/2623",
                                                new_time_stemp, xml=record_xml,
                                                oai_rec=oai_rec)
        assert record3 == {'pid': '1', 'title': 'Testovací záznam'}
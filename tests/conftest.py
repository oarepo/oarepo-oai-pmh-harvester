from __future__ import absolute_import, print_function

import pathlib
import shutil
import tempfile

import pytest
from flask import Flask, current_app
from flask_principal import Principal
from invenio_access import InvenioAccess
from invenio_accounts import InvenioAccounts
from invenio_base.signals import app_loaded
from invenio_db import InvenioDB
from invenio_db import db as db_
from invenio_indexer import InvenioIndexer
from invenio_indexer.api import RecordIndexer
from invenio_jsonschemas import InvenioJSONSchemas
from invenio_pidstore import InvenioPIDStore
from invenio_records import Record, InvenioRecords
from invenio_records_rest import InvenioRecordsREST
from invenio_records_rest.schemas.fields import SanitizedUnicode
from invenio_records_rest.utils import PIDConverter
from invenio_search import RecordsSearch, InvenioSearch
from lxml import etree
from marshmallow import Schema
from marshmallow.fields import Integer
from sqlalchemy_utils import database_exists, create_database

from oarepo_oai_pmh_harvester.ext import OArepoOAIClient
from oarepo_oai_pmh_harvester.views import oai_client_blueprint


class TestSchema(Schema):
    """Test record schema."""
    title = SanitizedUnicode()
    pid = Integer()


class TestRecord(Record):
    """Reference enabled test record class."""
    MARSHMALLOW_SCHEMA = TestSchema
    VALIDATE_MARSHMALLOW = True
    VALIDATE_PATCH = True

    @property
    def canonical_url(self):
        SERVER_NAME = current_app.config["SERVER_NAME"]
        return f"http://{SERVER_NAME}/api/records/{self['pid']}"
        # return url_for('invenio_records_rest.recid_item',
        #                pid_value=self['pid'], _external=True)


RECORDS_REST_ENDPOINTS = {
    'recid': dict(
        pid_type='recid',
        pid_minter='recid',
        pid_fetcher='recid',
        default_endpoint_prefix=True,
        search_class=RecordsSearch,
        indexer_class=RecordIndexer,
        search_index='records',
        search_type=None,
        record_serializers={
            'application/json': 'oarepo_validate:json_response',
        },
        search_serializers={
            'application/json': 'oarepo_validate:json_search',
        },
        record_loaders={
            'application/json': 'oarepo_validate:json_loader',
        },
        record_class=TestRecord,
        list_route='/records/',
        item_route='/records/<pid(recid):pid_value>',
        default_media_type='application/json',
        max_result_window=10000,
        error_handlers=dict()
    )
}


@pytest.yield_fixture()
def app():
    instance_path = tempfile.mkdtemp()
    app = Flask('testapp', instance_path=instance_path)

    app.config.update(
        JSONSCHEMAS_HOST="nusl.cz",
        SQLALCHEMY_TRACK_MODIFICATIONS=True,
        SERVER_NAME='127.0.0.1:5000',
        INVENIO_INSTANCE_PATH=instance_path,
        DEBUG=True,
        OAREPO_OAI_PROVIDERS={
            "uk": {
                "description": "Univerzita Karlova",
                "synchronizers": [
                    {
                        "name": "xoai",
                        "oai_endpoint": "https://dspace.cuni.cz/oai/nusl",
                        "set": "nusl_set",
                        "metadata_prefix": "xoai",
                        "unhandled_paths": ["/dc/unhandled"],
                        "default_endpoint": "recid",
                        "from": "latest",
                        # "use_default_endpoint": True,
                        "endpoint_mapping": {
                            "field_name": "doc_type",
                            "mapping": {
                                "record": "recid"
                            }
                        }
                    }
                ]
            },
        },
        RECORDS_REST_ENDPOINTS=RECORDS_REST_ENDPOINTS,
        PIDSTORE_RECID_FIELD='pid'
    )

    app.secret_key = 'changeme'

    InvenioDB(app)
    InvenioAccounts(app)
    InvenioAccess(app)
    Principal(app)
    InvenioJSONSchemas(app)
    InvenioSearch(app)
    InvenioIndexer(app)
    InvenioRecords(app)
    InvenioRecordsREST(app)
    InvenioPIDStore(app)
    app.url_map.converters['pid'] = PIDConverter
    OArepoOAIClient(app)
    # app.register_blueprint(oai_client_blueprint, url_prefix="/oai-client")
    print("\n\nURL MAP", app.url_map)

    app_loaded.send(app, app=app)

    with app.app_context():
        yield app

    shutil.rmtree(instance_path)


@pytest.fixture()
def db(app):
    """"Returns fresh db."""
    with app.app_context():
        if not database_exists(str(db_.engine.url)) and \
                app.config['SQLALCHEMY_DATABASE_URI'] != 'sqlite://':
            create_database(db_.engine.url)
        db_.create_all()

    yield db_

    # Explicitly close DB connection
    db_.session.close()
    db_.drop_all()


@pytest.fixture()
def metadata():
    return {
        "title": "Testovací záznam",
    }


@pytest.fixture()
def load_entry_points():
    import pkg_resources
    distribution = pkg_resources.Distribution(__file__)
    entry_point = pkg_resources.EntryPoint.parse('xoai = example.parser', dist=distribution)
    entry_point2 = pkg_resources.EntryPoint.parse('rule = example.rules.uk.rule', dist=distribution)
    entry_point3 = pkg_resources.EntryPoint.parse('handler = example.mapping', dist=distribution)
    entry_point4 = pkg_resources.EntryPoint.parse('pre_processor = example.pre_processors',
                                                  dist=distribution)
    entry_point5 = pkg_resources.EntryPoint.parse('post_processor = example.post_processors',
                                                  dist=distribution)
    distribution._ep_map = {
        'oarepo_oai_pmh_harvester.parsers': {'xoai': entry_point},
        'oarepo_oai_pmh_harvester.rules': {'rule': entry_point2},
        'oarepo_oai_pmh_harvester.mappings': {'handler': entry_point3},
        'oarepo_oai_pmh_harvester.pre_processors': {'pre_processor': entry_point4},
        'oarepo_oai_pmh_harvester.post_processors': {'post_processor': entry_point5},
    }
    pkg_resources.working_set.add(distribution)


@pytest.fixture()
def record_xml():
    dir_ = pathlib.Path(__file__).parent.absolute()
    path = dir_ / "data" / "test_xml.xml"
    with open(str(path), "r") as f:
        tree = etree.parse(f)
        return tree.getroot()


@pytest.fixture()
def parsed_record_xml():
    return {
        'dc': [
            {
                'title': [
                    {
                        'value': ['Testovací záznam']
                    }
                ],
                'unhandled': [
                    {
                        'value': ['Bla']
                    }
                ]
            }
        ]
    }

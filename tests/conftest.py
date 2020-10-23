from __future__ import absolute_import, print_function

import os
import pathlib
import shutil
import tempfile
from pathlib import Path

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
from sqlalchemy_utils import database_exists, drop_database, create_database

from oarepo_oai_pmh_harvester.ext import OArepoOAIClient


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
                        "use_default_endpoint": True,
                        "endpoint_mapping": {
                            "field_name": "doc_type",
                            "mapping": {
                                "record": "recid"
                            }
                        }
                    }
                ]
            }
        },
        RECORDS_REST_ENDPOINTS=RECORDS_REST_ENDPOINTS,
        PIDSTORE_RECID_FIELD='pid'
    )

    app.secret_key = 'changeme'
    print("\n\nINSTANCE PATH:", os.environ.get("INVENIO_INSTANCE_PATH"))

    InvenioDB(app)
    # OARepoReferences(app)
    InvenioAccounts(app)
    InvenioAccess(app)
    Principal(app)
    InvenioJSONSchemas(app)
    InvenioSearch(app)
    InvenioIndexer(app)
    # OARepoMappingIncludesExt(app)
    InvenioRecords(app)
    InvenioRecordsREST(app)
    # InvenioCelery(app)
    InvenioPIDStore(app)
    # Invenio Records Draft initialization
    # RecordsDraft(app)
    app.url_map.converters['pid'] = PIDConverter
    OArepoOAIClient(app)

    # # Celery
    # print(app.config["CELERY_BROKER_URL"])

    # login_manager = LoginManager()
    # login_manager.init_app(app)
    # login_manager.login_view = 'login'
    #
    # @login_manager.user_loader
    # def basic_user_loader(user_id):
    #     user_obj = User.query.get(int(user_id))
    #     return user_obj

    # app.register_blueprint(create_blueprint_from_app(app))

    # @app.route('/test/login/<int:id>', methods=['GET', 'POST'])
    # def test_login(id):
    #     print("test: logging user with id", id)
    #     response = make_response()
    #     user = User.query.get(id)
    #     login_user(user)
    #     set_identity(user)
    #     return response

    # app.extensions['invenio-search'].mappings["test"] = mapping
    # app.extensions["invenio-jsonschemas"].schemas["test"] = schema

    app_loaded.send(app, app=app)

    with app.app_context():
        # app.register_blueprint(taxonomies_blueprint)
        print(app.url_map)
        yield app

    shutil.rmtree(instance_path)


@pytest.fixture()
def db(app):
    """Create database for the tests."""
    dir_path = os.path.dirname(__file__)
    parent_path = str(Path(dir_path).parent)
    db_path = os.environ.get('SQLALCHEMY_DATABASE_URI', f'sqlite:////{parent_path}/database.db')
    os.environ["INVENIO_SQLALCHEMY_DATABASE_URI"] = db_path
    app.config.update(
        SQLALCHEMY_DATABASE_URI=db_path,
    )
    if database_exists(str(db_.engine.url)):
        drop_database(db_.engine.url)
    if not database_exists(str(db_.engine.url)):
        create_database(db_.engine.url)
    db_.create_all()

    #### TAXONOMIES
    # subprocess.run(["invenio", "taxonomies", "init"])
    # runner = app.test_cli_runner()
    # result = runner.invoke(init_db)
    # if result.exit_code:
    #     print(result.output, file=sys.stderr)
    # assert result.exit_code == 0
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
    distribution._ep_map = {
        'oarepo_oai_pmh_harvester.parsers': {'xoai': entry_point},
        'oarepo_oai_pmh_harvester.rules': {'rule': entry_point2}
    }
    pkg_resources.working_set.add(distribution)
    print(pkg_resources.working_set)


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

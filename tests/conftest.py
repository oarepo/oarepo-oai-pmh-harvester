from __future__ import absolute_import, print_function

import os
import pathlib
import shutil
import sys
import tempfile

import pytest
from flask import Flask
from flask_taxonomies import FlaskTaxonomies
from flask_taxonomies.views import blueprint as taxonomies_blueprint
from invenio_db import InvenioDB
from invenio_db import db as db_
from invenio_indexer import InvenioIndexer
from invenio_jsonschemas import InvenioJSONSchemas
from invenio_pidstore.models import PersistentIdentifier, Redirect
from invenio_records import InvenioRecords, Record
from invenio_records.models import RecordMetadata
from invenio_records_draft.cli import make_schemas
from invenio_records_draft.ext import InvenioRecordsDraft
from invenio_search import InvenioSearch
from lxml import etree
from sqlalchemy_utils import create_database, database_exists

from flask_taxonomies_es import FlaskTaxonomiesES
from invenio_nusl_theses import InvenioNUSLTheses
from invenio_oarepo_oai_pmh_harvester.models import OAIProvider, OAIRecord, OAISync
from invenio_oarepo_oai_pmh_harvester.synchronization import OAISynchronizer


@pytest.yield_fixture()
def app():
    instance_path = tempfile.mkdtemp()
    app = Flask('testapp', instance_path=instance_path)

    app.config.update(
        JSONSCHEMAS_HOST="nusl.cz",
        SQLALCHEMY_TRACK_MODIFICATIONS=True,
        SQLALCHEMY_DATABASE_URI=os.environ.get(
            'SQLALCHEMY_DATABASE_URI',
            'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user="oarepo", pw="oarepo",
                                                                  url="127.0.0.1",
                                                                  db="oarepo")),
        SERVER_NAME='127.0.0.1:5000',
    )
    InvenioRecordsDraft(app)
    InvenioJSONSchemas(app)
    InvenioRecords(app)
    InvenioSearch(app)
    InvenioIndexer(app)
    InvenioDB(app)
    FlaskTaxonomies(app)
    FlaskTaxonomiesES(app)
    InvenioNUSLTheses(app)
    with app.app_context():
        app.register_blueprint(taxonomies_blueprint)
        yield app

    shutil.rmtree(instance_path)


@pytest.yield_fixture()
def db(app):
    """Database fixture."""
    if not database_exists(str(db_.engine.url)):
        create_database(str(db_.engine.url))
    yield db_

    # Explicitly close DB connection
    db_.session.close()


@pytest.yield_fixture()
def uk_db(app):
    """Database fixture."""
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(
        user="oarepo", pw="oarepo", url="127.0.0.1", db="test_uk")
    if not database_exists(str(db_.engine.url)):
        create_database(str(db_.engine.url))
    Redirect.__table__.drop(db_.engine)
    PersistentIdentifier.__table__.drop(db_.engine)
    OAIRecord.__table__.drop(db_.engine)
    RecordMetadata.__table__.drop(db_.engine)
    OAISync.__table__.drop(db_.engine)
    db_.create_all()
    yield db_

    # Explicitly close DB connection
    db_.session.close()


@pytest.fixture
def test_db(app):
    """Create database for the tests."""
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
    if not database_exists(str(db_.engine.url)):
        create_database(db_.engine.url)
    db_.drop_all()
    db_.create_all()

    yield db_

    # Explicitly close DB connection
    db_.session.close()
    db_.drop_all()


@pytest.fixture()
def synchronizer_instance(app, test_db):
    provider = OAIProvider(
        code="uk",
        oai_endpoint="https://dspace.cuni.cz/oai/nusl",
        set_="nusl_set",
        metadata_prefix="xoai"
    )
    db_.session.add(provider)
    db_.session.commit()
    return OAISynchronizer(provider)


@pytest.fixture()
def record_xml():
    dir_ = pathlib.Path(__file__).parent.absolute()
    path = dir_ / "data" / "test_xml.xml"
    with open(str(path), "r") as f:
        tree = etree.parse(f)
        return tree.getroot()


@pytest.fixture()
def sample_record(app, test_db):
    record = Record.create(
        {
            "id": "1",
            "identifier": [
                {
                    "value": "oai:server:id",
                    "type": "originalOAI"
                }
            ]
        }
    )
    db_.session.commit()
    return record


@pytest.fixture()
def migrate_provider(app, test_db):
    provider = OAIProvider(
        code="nusl",
        description="Migration from old NUSL",
        oai_endpoint="https://invenio.nusl.cz/oai2d/"
    )
    db_.session.add(provider)
    db_.session.commit()
    return provider

@pytest.fixture
def schemas(app):
    runner = app.test_cli_runner()
    result = runner.invoke(make_schemas)
    if result.exit_code:
        print(result.output, file=sys.stderr)
    assert result.exit_code == 0

    # trigger registration of new schemas, normally performed
    # via app_loaded signal that is not emitted in tests
    with app.app_context():
        app.extensions['invenio-records-draft']._register_draft_schemas(app)
        app.extensions['invenio-records-draft']._register_draft_mappings(app)

    return {
        'published': 'https://localhost:5000/schemas/records/record-v1.0.0.json',
        'draft': 'https://localhost:5000/schemas/draft/records/record-v1.0.0.json',
    }

# @pytest.fixture
# def root_taxonomy(db):
#     """Create root taxonomy element."""
#     from flask_taxonomies.models import Taxonomy
#     root = Taxonomy.create_taxonomy(code="root")
#     db.session.add(root)
#     db.session.commit()
#     return root
#
#
# @pytest.fixture
# def sample_term(db, root_taxonomy):
#     """Taxonomy Term fixture."""
#     extra_data = {
#         "url": "http://www.vscht.cz/",
#         "title": [
#             {
#                 "lang": "cze",
#                 "value": "Vysoká škola chemicko-technologická v Praze"
#             }
#         ],
#         "address": "Technická 5, 166 28 Praha 6",
#         "lib_url": ""
#     }
#     term = root_taxonomy.create_term(slug="1", extra_data=extra_data)
#     db.session.add(term)
#     db.session.commit()
#     return term
#
#
# @pytest.fixture
# def child_term(db, root_taxonomy, sample_term):
#     extra_data = {
#         "title": [
#             {
#                 "lang": "cze",
#                 "value": "Dítě"
#             }
#         ]
#     }
#     term = sample_term.create_term(slug="3", extra_data=extra_data)
#     db.session.add(term)
#     db.session.commit()
#     return term
#
#
# @pytest.fixture()
# def csv_file():
#     fd, path = tempfile.mkstemp()
#     with os.fdopen(fd, 'w') as tmp:
#         writer = csv.writer(tmp)
#         writer.writerow(["sloupec1", "sloupec2", "sloupec3"])
#         for _ in range(25):
#             writer.writerow(["bla", "blah", "ble"])
#     yield path
#     os.remove(path)

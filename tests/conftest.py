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
from marshmallow.fields import Integer, Nested
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
                "oai_endpoint": "https://dspace.cuni.cz/oai/nusl",
                "set": "nusl_set",
                "metadata_prefix": "xoai",
                "unhandled_paths": ["/example/path"],
                "default_endpoint": "recid",
                "use_default_endpoint": True,
                "endpoint_mapping": {
                    "field_name": "doc_type",
                    "mapping": {
                        "record": "recid"
                    }
                }
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
        'bundles': [{
                        'bundle': [{
                                       'bitstreams': [{
                                                          'bitstream': [{
                                                                            'checksum': [
                                                                                '2de77554460e124aa955ec4906b27574'],
                                                                            'checksumAlgorithm': [
                                                                                'MD5'],
                                                                            'description': [
                                                                                'Extracted '
                                                                                'text'],
                                                                            'format': [
                                                                                'text/plain'],
                                                                            'name': [
                                                                                'DPTX_2005_2_11410_OSZD001_67587_0_20611.pdf.txt'],
                                                                            'originalName': [
                                                                                'DPTX_2005_2_11410_OSZD001_67587_0_20611.pdf.txt'],
                                                                            'sid': ['7'],
                                                                            'size': ['121688'],
                                                                            'url': ['\n'
                                                                                    '             '
                                                                                    '             '
                                                                                    '      '
                                                                                    'https://dspace.cuni.cz/bitstream/20.500.11956/2623/7/DPTX_2005_2_11410_OSZD001_67587_0_20611.pdf.txt\n'
                                                                                    '             '
                                                                                    '             '
                                                                                    '  ']
                                                                        },
                                                                        {
                                                                            'checksum': [
                                                                                '824c83826460b4b93efd3a86f4610a33'],
                                                                            'checksumAlgorithm': [
                                                                                'MD5'],
                                                                            'description': [
                                                                                'Extracted '
                                                                                'text'],
                                                                            'format': [
                                                                                'text/plain'],
                                                                            'name': [
                                                                                'DPBC_2005_2_11410_OSZD001_67587_0_20611.pdf.txt'],
                                                                            'originalName': [
                                                                                'DPBC_2005_2_11410_OSZD001_67587_0_20611.pdf.txt'],
                                                                            'sid': ['8'],
                                                                            'size': ['1421'],
                                                                            'url': ['\n'
                                                                                    '             '
                                                                                    '             '
                                                                                    '      '
                                                                                    'https://dspace.cuni.cz/bitstream/20.500.11956/2623/8/DPBC_2005_2_11410_OSZD001_67587_0_20611.pdf.txt\n'
                                                                                    '             '
                                                                                    '             '
                                                                                    '  ']
                                                                        },
                                                                        {
                                                                            'checksum': [
                                                                                '824c83826460b4b93efd3a86f4610a33'],
                                                                            'checksumAlgorithm': [
                                                                                'MD5'],
                                                                            'description': [
                                                                                'Extracted '
                                                                                'text'],
                                                                            'format': [
                                                                                'text/plain'],
                                                                            'name': [
                                                                                'DPBE_2005_2_11410_OSZD001_67587_0_20611.pdf.txt'],
                                                                            'originalName': [
                                                                                'DPBE_2005_2_11410_OSZD001_67587_0_20611.pdf.txt'],
                                                                            'sid': ['9'],
                                                                            'size': ['1421'],
                                                                            'url': ['\n'
                                                                                    '             '
                                                                                    '             '
                                                                                    '      '
                                                                                    'https://dspace.cuni.cz/bitstream/20.500.11956/2623/9/DPBE_2005_2_11410_OSZD001_67587_0_20611.pdf.txt\n'
                                                                                    '             '
                                                                                    '             '
                                                                                    '  ']
                                                                        },
                                                                        {
                                                                            'checksum': [
                                                                                '386a8671b9361cd1cb3bbe020c5ffc69'],
                                                                            'checksumAlgorithm': [
                                                                                'MD5'],
                                                                            'description': [
                                                                                'Extracted '
                                                                                'text'],
                                                                            'format': [
                                                                                'text/plain'],
                                                                            'name': [
                                                                                'DPPV_2005_2_11410_OSZD001_67587_0_20611.pdf.txt'],
                                                                            'originalName': [
                                                                                'DPPV_2005_2_11410_OSZD001_67587_0_20611.pdf.txt'],
                                                                            'sid': ['10'],
                                                                            'size': ['2979'],
                                                                            'url': ['\n'
                                                                                    '             '
                                                                                    '             '
                                                                                    '      '
                                                                                    'https://dspace.cuni.cz/bitstream/20.500.11956/2623/10/DPPV_2005_2_11410_OSZD001_67587_0_20611.pdf.txt\n'
                                                                                    '             '
                                                                                    '             '
                                                                                    '  ']
                                                                        },
                                                                        {
                                                                            'checksum': [
                                                                                'e9d61122e5b83af1ec0a9e6a7831079c'],
                                                                            'checksumAlgorithm': [
                                                                                'MD5'],
                                                                            'description': [
                                                                                'Extracted '
                                                                                'text'],
                                                                            'format': [
                                                                                'text/plain'],
                                                                            'name': [
                                                                                'DPPO_2005_2_11410_OSZD001_67587_0_20611.pdf.txt'],
                                                                            'originalName': [
                                                                                'DPPO_2005_2_11410_OSZD001_67587_0_20611.pdf.txt'],
                                                                            'sid': ['11'],
                                                                            'size': ['3167'],
                                                                            'url': ['\n'
                                                                                    '             '
                                                                                    '             '
                                                                                    '      '
                                                                                    'https://dspace.cuni.cz/bitstream/20.500.11956/2623/11/DPPO_2005_2_11410_OSZD001_67587_0_20611.pdf.txt\n'
                                                                                    '             '
                                                                                    '             '
                                                                                    '  ']
                                                                        }]
                                                      }],
                                       'name': ['TEXT']
                                   },
                                   {
                                       'bitstreams': [{
                                                          'bitstream': [{
                                                                            'checksum': [
                                                                                'ec1020c2c1319cfb23454e4a80c76624'],
                                                                            'checksumAlgorithm': [
                                                                                'MD5'],
                                                                            'description': [
                                                                                'Náhledový '
                                                                                'obrázek'],
                                                                            'format': ['image/png'],
                                                                            'name': [
                                                                                'thumbnail.png'],
                                                                            'sid': ['6'],
                                                                            'size': ['21344'],
                                                                            'url': [
                                                                                'https://dspace.cuni.cz/bitstream/20.500.11956/2623/6/thumbnail.png']
                                                                        }]
                                                      }],
                                       'name': ['THUMBNAIL']
                                   },
                                   {
                                       'bitstreams': [{
                                                          'bitstream': [{
                                                                            'checksum': [
                                                                                'c09f13bbfd40f8a0c029f059f8e0eae5'],
                                                                            'checksumAlgorithm': [
                                                                                'MD5'],
                                                                            'description': ['Text '
                                                                                            'práce'],
                                                                            'format': [
                                                                                'application/pdf'],
                                                                            'name': [
                                                                                'DPTX_2005_2_11410_OSZD001_67587_0_20611.pdf'],
                                                                            'sid': ['1'],
                                                                            'size': ['14129928'],
                                                                            'url': ['\n'
                                                                                    '             '
                                                                                    '             '
                                                                                    '      '
                                                                                    'https://dspace.cuni.cz/bitstream/20.500.11956/2623/1/DPTX_2005_2_11410_OSZD001_67587_0_20611.pdf\n'
                                                                                    '             '
                                                                                    '             '
                                                                                    '  ']
                                                                        },
                                                                        {
                                                                            'checksum': [
                                                                                'dc442bc11a081392c9528775bb18d0e9'],
                                                                            'checksumAlgorithm': [
                                                                                'MD5'],
                                                                            'description': [
                                                                                'Abstrakt'],
                                                                            'format': [
                                                                                'application/pdf'],
                                                                            'name': [
                                                                                'DPBC_2005_2_11410_OSZD001_67587_0_20611.pdf'],
                                                                            'sid': ['2'],
                                                                            'size': ['81938'],
                                                                            'url': ['\n'
                                                                                    '             '
                                                                                    '             '
                                                                                    '      '
                                                                                    'https://dspace.cuni.cz/bitstream/20.500.11956/2623/2/DPBC_2005_2_11410_OSZD001_67587_0_20611.pdf\n'
                                                                                    '             '
                                                                                    '             '
                                                                                    '  ']
                                                                        },
                                                                        {
                                                                            'checksum': [
                                                                                '5e5109bf584190086414c0dc6e4b8d93'],
                                                                            'checksumAlgorithm': [
                                                                                'MD5'],
                                                                            'description': [
                                                                                'Abstrakt '
                                                                                '(anglicky)'],
                                                                            'format': [
                                                                                'application/pdf'],
                                                                            'name': [
                                                                                'DPBE_2005_2_11410_OSZD001_67587_0_20611.pdf'],
                                                                            'sid': ['3'],
                                                                            'size': ['81938'],
                                                                            'url': ['\n'
                                                                                    '             '
                                                                                    '             '
                                                                                    '      '
                                                                                    'https://dspace.cuni.cz/bitstream/20.500.11956/2623/3/DPBE_2005_2_11410_OSZD001_67587_0_20611.pdf\n'
                                                                                    '             '
                                                                                    '             '
                                                                                    '  ']
                                                                        },
                                                                        {
                                                                            'checksum': [
                                                                                '96f8f75445d061231c6b519657ea0fb8'],
                                                                            'checksumAlgorithm': [
                                                                                'MD5'],
                                                                            'description': [
                                                                                'Posudek '
                                                                                'vedoucího'],
                                                                            'format': [
                                                                                'application/pdf'],
                                                                            'name': [
                                                                                'DPPV_2005_2_11410_OSZD001_67587_0_20611.pdf'],
                                                                            'sid': ['4'],
                                                                            'size': ['187174'],
                                                                            'url': ['\n'
                                                                                    '             '
                                                                                    '             '
                                                                                    '      '
                                                                                    'https://dspace.cuni.cz/bitstream/20.500.11956/2623/4/DPPV_2005_2_11410_OSZD001_67587_0_20611.pdf\n'
                                                                                    '             '
                                                                                    '             '
                                                                                    '  ']
                                                                        },
                                                                        {
                                                                            'checksum': [
                                                                                '8cb8b7459d50ffe4809cc1a94243f493'],
                                                                            'checksumAlgorithm': [
                                                                                'MD5'],
                                                                            'description': [
                                                                                'Posudek '
                                                                                'oponenta'],
                                                                            'format': [
                                                                                'application/pdf'],
                                                                            'name': [
                                                                                'DPPO_2005_2_11410_OSZD001_67587_0_20611.pdf'],
                                                                            'sid': ['5'],
                                                                            'size': ['193346'],
                                                                            'url': ['\n'
                                                                                    '             '
                                                                                    '             '
                                                                                    '      '
                                                                                    'https://dspace.cuni.cz/bitstream/20.500.11956/2623/5/DPPO_2005_2_11410_OSZD001_67587_0_20611.pdf\n'
                                                                                    '             '
                                                                                    '             '
                                                                                    '  ']
                                                                        }]
                                                      }],
                                       'name': ['ORIGINAL']
                                   }]
                    }],
        'dc': [{
                   'contributor': [{
                                       'advisor': [{'value': [['Kubíčková, Věra']]}],
                                       'referee': [{'value': [['Hronzová, Marie']]}]
                                   }],
                   'creator': [{'value': [['Smolková, Lenka']]}],
                   'date': [{
                                'accessioned': [{'value': [['2017-03-17T09:30:02Z']]}],
                                'available': [{'value': [['2017-03-17T09:30:02Z']]}],
                                'issued': [{'value': [['2006']]}]
                            }],
                   'description': [{
                                       'abstract': [{
                                                        'cs_CZ': [{
                                                                      'value': ['Ze života lidí '
                                                                                'se stále vytrácí '
                                                                                'přirozený pohyb. '
                                                                                'Vymoženosti '
                                                                                'současné\n'
                                                                                '                 '
                                                                                '               '
                                                                                'společnosti ( '
                                                                                'televize, '
                                                                                'počítače...) '
                                                                                'tyto trendy '
                                                                                'návyku snížené '
                                                                                'potřeby pohybu '
                                                                                'jen\n'
                                                                                '                 '
                                                                                '               '
                                                                                'podporují. '
                                                                                '&quot;Změnil se '
                                                                                'charakter, '
                                                                                'zaměření, účel a '
                                                                                'cíl pohybových '
                                                                                'aktivit, došlo\n'
                                                                                '                 '
                                                                                '               '
                                                                                'kjejich značné '
                                                                                'diferenciaci a '
                                                                                'disproporci mezi '
                                                                                'aktivními a '
                                                                                'pasivními '
                                                                                'účastníky. '
                                                                                'Objevují\n'
                                                                                '                 '
                                                                                '               '
                                                                                'se nepřiměřené '
                                                                                'emoce až '
                                                                                'hysterie v '
                                                                                'souvislosti se '
                                                                                'sportovními '
                                                                                'akcemi, '
                                                                                'uctívání\n'
                                                                                '                 '
                                                                                '               '
                                                                                'silnějších, '
                                                                                'dravějších, '
                                                                                'případně i '
                                                                                'bohatších.&quot; '
                                                                                '(9) Je nezbytné, '
                                                                                'aby tělesná\n'
                                                                                '                 '
                                                                                '               '
                                                                                'zdatnost a její '
                                                                                'význam byla '
                                                                                'vnímána lidmi '
                                                                                'jako důležitá '
                                                                                'životní hodnota. '
                                                                                'Vždyť přiměřeně\n'
                                                                                '                 '
                                                                                '               '
                                                                                'tělesně zdatný '
                                                                                'člověk, navíc '
                                                                                'pohybově '
                                                                                'kultivovaný, se '
                                                                                'v praktickém '
                                                                                'životě spolu s\n'
                                                                                '                 '
                                                                                '               '
                                                                                'mravními postoji '
                                                                                'a vzdělaností '
                                                                                'přibližuje k '
                                                                                'ideálu '
                                                                                'všestranně '
                                                                                'rozvinutého '
                                                                                'člověka. V\n'
                                                                                '                 '
                                                                                '               '
                                                                                'lidském životě '
                                                                                'hraje '
                                                                                'nejvýznamnější '
                                                                                'období pro '
                                                                                'účinný tělesný a '
                                                                                'pohybový rozvoj '
                                                                                'školní\n'
                                                                                '                 '
                                                                                '               '
                                                                                'věk. Právě v '
                                                                                'dětském věku je '
                                                                                'podpůrně '
                                                                                'pohybový systém '
                                                                                'velmi citlivý na '
                                                                                'nepřiměřenou\n'
                                                                                '                 '
                                                                                '               '
                                                                                'strukturu '
                                                                                'tělesné zátěže a '
                                                                                'nedostatek '
                                                                                'pohybové '
                                                                                'aktivity. Nelze '
                                                                                'přehlédnout, že '
                                                                                'značný\n'
                                                                                '                 '
                                                                                '               '
                                                                                'počet dětí '
                                                                                'projevuje nízkou '
                                                                                'tělesnou '
                                                                                'zdatnost a také '
                                                                                'nedostatečné '
                                                                                'zvládnutí pro '
                                                                                'život\n'
                                                                                '                 '
                                                                                '               '
                                                                                'důležitých '
                                                                                'pohybových '
                                                                                'dovedností. '
                                                                                'Kolisko uvádí '
                                                                                '(7, str.5), že '
                                                                                '20% dětí '
                                                                                'předškolního\n'
                                                                                '                 '
                                                                                '               '
                                                                                'věku trpí vadným '
                                                                                'držením těla a v '
                                                                                'období 11-12 let '
                                                                                'je tento stav '
                                                                                'téměř '
                                                                                'trojnásobný.\n'
                                                                                '                 '
                                                                                '           ']
                                                                  }],
                                                        'en_US': [{
                                                                      'value': ['Ze života lidí '
                                                                                'se stále vytrácí '
                                                                                'přirozený pohyb. '
                                                                                'Vymoženosti '
                                                                                'současné\n'
                                                                                '                 '
                                                                                '               '
                                                                                'společnosti ( '
                                                                                'televize, '
                                                                                'počítače...) '
                                                                                'tyto trendy '
                                                                                'návyku snížené '
                                                                                'potřeby pohybu '
                                                                                'jen\n'
                                                                                '                 '
                                                                                '               '
                                                                                'podporují. '
                                                                                '&quot;Změnil se '
                                                                                'charakter, '
                                                                                'zaměření, účel a '
                                                                                'cíl pohybových '
                                                                                'aktivit, došlo\n'
                                                                                '                 '
                                                                                '               '
                                                                                'kjejich značné '
                                                                                'diferenciaci a '
                                                                                'disproporci mezi '
                                                                                'aktivními a '
                                                                                'pasivními '
                                                                                'účastníky. '
                                                                                'Objevují\n'
                                                                                '                 '
                                                                                '               '
                                                                                'se nepřiměřené '
                                                                                'emoce až '
                                                                                'hysterie v '
                                                                                'souvislosti se '
                                                                                'sportovními '
                                                                                'akcemi, '
                                                                                'uctívání\n'
                                                                                '                 '
                                                                                '               '
                                                                                'silnějších, '
                                                                                'dravějších, '
                                                                                'případně i '
                                                                                'bohatších.&quot; '
                                                                                '(9) Je nezbytné, '
                                                                                'aby tělesná\n'
                                                                                '                 '
                                                                                '               '
                                                                                'zdatnost a její '
                                                                                'význam byla '
                                                                                'vnímána lidmi '
                                                                                'jako důležitá '
                                                                                'životní hodnota. '
                                                                                'Vždyť přiměřeně\n'
                                                                                '                 '
                                                                                '               '
                                                                                'tělesně zdatný '
                                                                                'člověk, navíc '
                                                                                'pohybově '
                                                                                'kultivovaný, se '
                                                                                'v praktickém '
                                                                                'životě spolu s\n'
                                                                                '                 '
                                                                                '               '
                                                                                'mravními postoji '
                                                                                'a vzdělaností '
                                                                                'přibližuje k '
                                                                                'ideálu '
                                                                                'všestranně '
                                                                                'rozvinutého '
                                                                                'člověka. V\n'
                                                                                '                 '
                                                                                '               '
                                                                                'lidském životě '
                                                                                'hraje '
                                                                                'nejvýznamnější '
                                                                                'období pro '
                                                                                'účinný tělesný a '
                                                                                'pohybový rozvoj '
                                                                                'školní\n'
                                                                                '                 '
                                                                                '               '
                                                                                'věk. Právě v '
                                                                                'dětském věku je '
                                                                                'podpůrně '
                                                                                'pohybový systém '
                                                                                'velmi citlivý na '
                                                                                'nepřiměřenou\n'
                                                                                '                 '
                                                                                '               '
                                                                                'strukturu '
                                                                                'tělesné zátěže a '
                                                                                'nedostatek '
                                                                                'pohybové '
                                                                                'aktivity. Nelze '
                                                                                'přehlédnout, že '
                                                                                'značný\n'
                                                                                '                 '
                                                                                '               '
                                                                                'počet dětí '
                                                                                'projevuje nízkou '
                                                                                'tělesnou '
                                                                                'zdatnost a také '
                                                                                'nedostatečné '
                                                                                'zvládnutí pro '
                                                                                'život\n'
                                                                                '                 '
                                                                                '               '
                                                                                'důležitých '
                                                                                'pohybových '
                                                                                'dovedností. '
                                                                                'Kolisko uvádí '
                                                                                '(7, str.5), že '
                                                                                '20% dětí '
                                                                                'předškolního\n'
                                                                                '                 '
                                                                                '               '
                                                                                'věku trpí vadným '
                                                                                'držením těla a v '
                                                                                'období 11-12 let '
                                                                                'je tento stav '
                                                                                'téměř '
                                                                                'trojnásobný.\n'
                                                                                '                 '
                                                                                '           ']
                                                                  }]
                                                    }],
                                       'department': [{
                                                          'cs_CZ': [{
                                                                        'value': ['Katedra '
                                                                                  'tělesné '
                                                                                  'výchovy']
                                                                    }]
                                                      }],
                                       'faculty': [{
                                                       'cs_CZ': [{
                                                                     'value': ['Pedagogická '
                                                                               'fakulta']
                                                                 }],
                                                       'en_US': [{
                                                                     'value': ['Faculty of '
                                                                               'Education']
                                                                 }]
                                                   }],
                                       'provenance': [{
                                                          'en': [{
                                                                     'value': ['Made available in '
                                                                               'DSpace on '
                                                                               '2017-03-17T09:30:02Z '
                                                                               '(GMT). No. of\n'
                                                                               '                  '
                                                                               '              '
                                                                               'bitstreams: 6\n'
                                                                               '                  '
                                                                               '              '
                                                                               'DPTX_2005_2_11410_OSZD001_67587_0_20611.pdf: '
                                                                               '14129928 bytes, '
                                                                               'checksum:\n'
                                                                               '                  '
                                                                               '              '
                                                                               'c09f13bbfd40f8a0c029f059f8e0eae5 '
                                                                               '(MD5)\n'
                                                                               '                  '
                                                                               '              '
                                                                               'DPBC_2005_2_11410_OSZD001_67587_0_20611.pdf: '
                                                                               '81938 bytes, '
                                                                               'checksum:\n'
                                                                               '                  '
                                                                               '              '
                                                                               'dc442bc11a081392c9528775bb18d0e9 '
                                                                               '(MD5)\n'
                                                                               '                  '
                                                                               '              '
                                                                               'DPBE_2005_2_11410_OSZD001_67587_0_20611.pdf: '
                                                                               '81938 bytes, '
                                                                               'checksum:\n'
                                                                               '                  '
                                                                               '              '
                                                                               '5e5109bf584190086414c0dc6e4b8d93 '
                                                                               '(MD5)\n'
                                                                               '                  '
                                                                               '              '
                                                                               'DPPV_2005_2_11410_OSZD001_67587_0_20611.pdf: '
                                                                               '187174 bytes, '
                                                                               'checksum:\n'
                                                                               '                  '
                                                                               '              '
                                                                               '96f8f75445d061231c6b519657ea0fb8 '
                                                                               '(MD5)\n'
                                                                               '                  '
                                                                               '              '
                                                                               'DPPO_2005_2_11410_OSZD001_67587_0_20611.pdf: '
                                                                               '193346 bytes, '
                                                                               'checksum:\n'
                                                                               '                  '
                                                                               '              '
                                                                               '8cb8b7459d50ffe4809cc1a94243f493 '
                                                                               '(MD5)\n'
                                                                               '                  '
                                                                               '              '
                                                                               'thumbnail.png: '
                                                                               '21344 bytes, '
                                                                               'checksum: '
                                                                               'ec1020c2c1319cfb23454e4a80c76624 '
                                                                               '(MD5)\n'
                                                                               '                  '
                                                                               '          ']
                                                                 }]
                                                      }]
                                   }],
                   'identifier': [{
                                      'aleph': [{'value': [['000572336']]}],
                                      'repId': [{'value': [['20611']]}],
                                      'uri': [
                                          {'value': [['http://hdl.handle.net/20.500.11956/2623']]}]
                                  }],
                   'language': [{
                                    'cs_CZ': [{'value': ['Čeština']}],
                                    'iso': [{'value': [['cs_CZ']]}]
                                }],
                   'publisher': [{
                                     'cs_CZ': [{
                                                   'value': ['Univerzita Karlova, Pedagogická '
                                                             'fakulta']
                                               }]
                                 }],
                   'title': [{
                                 'cs_CZ': [{
                                               'value': ['Zdravotní tělesná výchova na '
                                                         'základních školách v Plzni a '
                                                         'okolí']
                                           }],
                                 'translated': [{
                                                    'en_US': [{
                                                                  'value': ['Physical Education '
                                                                            'at Basic Schools in '
                                                                            'Pilsen and the '
                                                                            'Surrounding\n'
                                                                            '                                '
                                                                            'Areas\n'
                                                                            '                            ']
                                                              }]
                                                }]
                             }],
                   'type': [{'cs_CZ': [{'value': ['diplomová práce']}]}]
               }],
        'dcterms': [{
                        'created': [{'value': [['2006']]}],
                        'dateAccepted': [{'value': [['2006-01-17']]}]
                    }],
        'others': [{
                       'handle': ['20.500.11956/2623'],
                       'identifier': ['oai:dspace.cuni.cz:20.500.11956/2623'],
                       'lastModifyDate': ['2017-09-11 10:12:53.118']
                   }],
        'repository': [{'mail': ['dspace@is.cuni.cz'], 'name': ['DSpace Repozitář']}],
        'thesis': [{
                       'degree': [{
                                      'discipline': [{
                                                         'cs_CZ': [{
                                                                       'value': ['Učitelství pro '
                                                                                 '1. stupeň '
                                                                                 'základní '
                                                                                 'školy']
                                                                   }],
                                                         'en_US': [{
                                                                       'value': ['Teacher '
                                                                                 'Training for '
                                                                                 'Primary '
                                                                                 'Schools']
                                                                   }]
                                                     }],
                                      'level': [{'cs_CZ': [{'value': ['magisterské']}]}],
                                      'name': [{'value': [['Mgr.']]}],
                                      'program': [{
                                                      'cs_CZ': [{
                                                                    'value': ['Učitelství pro '
                                                                              'základní školy']
                                                                }],
                                                      'en_US': [{
                                                                    'value': ['Teacher Training '
                                                                              'for Primary '
                                                                              'Schools']
                                                                }]
                                                  }]
                                  }],
                       'grade': [{
                                     'cs': [{'cs_CZ': [{'value': ['Výborně']}]}],
                                     'en': [{'en_US': [{'value': ['Excellent']}]}]
                                 }]
                   }],
        'uk': [{
                   'abstract': [{
                                    'cs': [{
                                               'cs_CZ': [{
                                                             'value': ['Ze života lidí se stále '
                                                                       'vytrácí přirozený pohyb. '
                                                                       'Vymoženosti současné\n'
                                                                       '                                '
                                                                       'společnosti ( televize, '
                                                                       'počítače...) tyto trendy '
                                                                       'návyku snížené potřeby '
                                                                       'pohybu jen\n'
                                                                       '                                '
                                                                       'podporují. &quot;Změnil '
                                                                       'se charakter, zaměření, '
                                                                       'účel a cíl pohybových '
                                                                       'aktivit, došlo\n'
                                                                       '                                '
                                                                       'kjejich značné '
                                                                       'diferenciaci a '
                                                                       'disproporci mezi '
                                                                       'aktivními a pasivními '
                                                                       'účastníky. Objevují\n'
                                                                       '                                '
                                                                       'se nepřiměřené emoce až '
                                                                       'hysterie v souvislosti se '
                                                                       'sportovními akcemi, '
                                                                       'uctívání\n'
                                                                       '                                '
                                                                       'silnějších, dravějších, '
                                                                       'případně i '
                                                                       'bohatších.&quot; (9) Je '
                                                                       'nezbytné, aby tělesná\n'
                                                                       '                                '
                                                                       'zdatnost a její význam '
                                                                       'byla vnímána lidmi jako '
                                                                       'důležitá životní hodnota. '
                                                                       'Vždyť přiměřeně\n'
                                                                       '                                '
                                                                       'tělesně zdatný člověk, '
                                                                       'navíc pohybově '
                                                                       'kultivovaný, se v '
                                                                       'praktickém životě spolu '
                                                                       's\n'
                                                                       '                                '
                                                                       'mravními postoji a '
                                                                       'vzdělaností přibližuje k '
                                                                       'ideálu všestranně '
                                                                       'rozvinutého člověka. V\n'
                                                                       '                                '
                                                                       'lidském životě hraje '
                                                                       'nejvýznamnější období pro '
                                                                       'účinný tělesný a pohybový '
                                                                       'rozvoj školní\n'
                                                                       '                                '
                                                                       'věk. Právě v dětském věku '
                                                                       'je podpůrně pohybový '
                                                                       'systém velmi citlivý na '
                                                                       'nepřiměřenou\n'
                                                                       '                                '
                                                                       'strukturu tělesné zátěže '
                                                                       'a nedostatek pohybové '
                                                                       'aktivity. Nelze '
                                                                       'přehlédnout, že značný\n'
                                                                       '                                '
                                                                       'počet dětí projevuje '
                                                                       'nízkou tělesnou zdatnost '
                                                                       'a také nedostatečné '
                                                                       'zvládnutí pro život\n'
                                                                       '                                '
                                                                       'důležitých pohybových '
                                                                       'dovedností. Kolisko uvádí '
                                                                       '(7, str.5), že 20% dětí '
                                                                       'předškolního\n'
                                                                       '                                '
                                                                       'věku trpí vadným držením '
                                                                       'těla a v období 11-12 let '
                                                                       'je tento stav téměř '
                                                                       'trojnásobný.\n'
                                                                       '                            ']
                                                         }]
                                           }],
                                    'en': [{
                                               'en_US': [{
                                                             'value': ['Ze života lidí se stále '
                                                                       'vytrácí přirozený pohyb. '
                                                                       'Vymoženosti současné\n'
                                                                       '                                '
                                                                       'společnosti ( televize, '
                                                                       'počítače...) tyto trendy '
                                                                       'návyku snížené potřeby '
                                                                       'pohybu jen\n'
                                                                       '                                '
                                                                       'podporují. &quot;Změnil '
                                                                       'se charakter, zaměření, '
                                                                       'účel a cíl pohybových '
                                                                       'aktivit, došlo\n'
                                                                       '                                '
                                                                       'kjejich značné '
                                                                       'diferenciaci a '
                                                                       'disproporci mezi '
                                                                       'aktivními a pasivními '
                                                                       'účastníky. Objevují\n'
                                                                       '                                '
                                                                       'se nepřiměřené emoce až '
                                                                       'hysterie v souvislosti se '
                                                                       'sportovními akcemi, '
                                                                       'uctívání\n'
                                                                       '                                '
                                                                       'silnějších, dravějších, '
                                                                       'případně i '
                                                                       'bohatších.&quot; (9) Je '
                                                                       'nezbytné, aby tělesná\n'
                                                                       '                                '
                                                                       'zdatnost a její význam '
                                                                       'byla vnímána lidmi jako '
                                                                       'důležitá životní hodnota. '
                                                                       'Vždyť přiměřeně\n'
                                                                       '                                '
                                                                       'tělesně zdatný člověk, '
                                                                       'navíc pohybově '
                                                                       'kultivovaný, se v '
                                                                       'praktickém životě spolu '
                                                                       's\n'
                                                                       '                                '
                                                                       'mravními postoji a '
                                                                       'vzdělaností přibližuje k '
                                                                       'ideálu všestranně '
                                                                       'rozvinutého člověka. V\n'
                                                                       '                                '
                                                                       'lidském životě hraje '
                                                                       'nejvýznamnější období pro '
                                                                       'účinný tělesný a pohybový '
                                                                       'rozvoj školní\n'
                                                                       '                                '
                                                                       'věk. Právě v dětském věku '
                                                                       'je podpůrně pohybový '
                                                                       'systém velmi citlivý na '
                                                                       'nepřiměřenou\n'
                                                                       '                                '
                                                                       'strukturu tělesné zátěže '
                                                                       'a nedostatek pohybové '
                                                                       'aktivity. Nelze '
                                                                       'přehlédnout, že značný\n'
                                                                       '                                '
                                                                       'počet dětí projevuje '
                                                                       'nízkou tělesnou zdatnost '
                                                                       'a také nedostatečné '
                                                                       'zvládnutí pro život\n'
                                                                       '                                '
                                                                       'důležitých pohybových '
                                                                       'dovedností. Kolisko uvádí '
                                                                       '(7, str.5), že 20% dětí '
                                                                       'předškolního\n'
                                                                       '                                '
                                                                       'věku trpí vadným držením '
                                                                       'těla a v období 11-12 let '
                                                                       'je tento stav téměř '
                                                                       'trojnásobný.\n'
                                                                       '                            ']
                                                         }]
                                           }]
                                }],
                   'degree-discipline': [{
                                             'cs': [{
                                                        'cs_CZ': [{
                                                                      'value': ['Učitelství pro '
                                                                                '1. stupeň '
                                                                                'základní '
                                                                                'školy']
                                                                  }]
                                                    }],
                                             'en': [{
                                                        'en_US': [{
                                                                      'value': ['Teacher Training '
                                                                                'for Primary '
                                                                                'Schools']
                                                                  }]
                                                    }]
                                         }],
                   'degree-program': [{
                                          'cs': [{
                                                     'cs_CZ': [{
                                                                   'value': ['Učitelství pro '
                                                                             'základní školy']
                                                               }]
                                                 }],
                                          'en': [{
                                                     'en_US': [{
                                                                   'value': ['Teacher Training '
                                                                             'for Primary '
                                                                             'Schools']
                                                               }]
                                                 }]
                                      }],
                   'faculty-abbr': [{'cs': [{'cs_CZ': [{'value': ['PedF']}]}]}],
                   'faculty-name': [{
                                        'cs': [{
                                                   'cs_CZ': [{
                                                                 'value': ['Pedagogická '
                                                                           'fakulta']
                                                             }]
                                               }],
                                        'en': [{
                                                   'en_US': [{
                                                                 'value': ['Faculty of '
                                                                           'Education']
                                                             }]
                                               }]
                                    }],
                   'grantor': [{
                                   'cs_CZ': [{
                                                 'value': ['Univerzita Karlova, Pedagogická '
                                                           'fakulta, Katedra tělesné '
                                                           'výchovy']
                                             }]
                               }],
                   'publication-place': [{'cs_CZ': [{'value': ['Praha']}]}],
                   'taxonomy': [{
                                    'organization-cs': [{
                                                            'cs_CZ': [{
                                                                          'value': ['Pedagogická '
                                                                                    'fakulta::Katedra '
                                                                                    'tělesné '
                                                                                    'výchovy']
                                                                      }]
                                                        }]
                                }],
                   'thesis': [{'type': [{'cs_CZ': [{'value': ['diplomová práce']}]}]}]
               }]
    }

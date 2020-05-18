import random
from datetime import datetime
from unittest.mock import MagicMock

import pytest
from sickle import Sickle
from sickle.iterator import OAIItemIterator

from invenio_oarepo_oai_pmh_harvester.exceptions import HandlerNotFoundError
from invenio_oarepo_oai_pmh_harvester.models import OAISync
from invenio_oarepo_oai_pmh_harvester.register import Decorators
from invenio_oarepo_oai_pmh_harvester.synchronization import OAISynchronizer


def test_init(app, test_db, migrate_provider):
    synchronizer = OAISynchronizer(migrate_provider)
    assert synchronizer is not None


def test_delete(migrate_provider):
    def delete_handler(oai_identifier):
        pass

    synchronizer = OAISynchronizer(migrate_provider, delete_record=delete_handler)
    synchronizer.delete("bla")


def test_delete_2(migrate_provider):
    synchronizer = OAISynchronizer(migrate_provider)
    with pytest.raises(HandlerNotFoundError):
        synchronizer.delete("bla")


def test_synchronize_delete(migrate_provider):
    def delete_handler(oai_identifier, datestamp):
        print("deleted")

    class Identifier:
        datestamp = datetime.utcnow()
        identifier = random.randint(0, 100000)
        deleted = True

    identifiers = [Identifier() for x in range(10)]
    synchronizer = OAISynchronizer(migrate_provider, delete_record=delete_handler)
    synchronizer.synchronize(identifiers=identifiers)
    assert synchronizer.deleted == 10


def test_synchronize_create(migrate_provider, record_xml, sample_record):
    class Record:
        xml = record_xml

    def create_handler(*args, **kwargs):
        return sample_record.id

    @Decorators.parser("test_parser", "nusl")
    def parser(*args, **kwargs):
        return {
            "id": "1",
            "title": "Some title",
            "language": ["cze", "eng"]
        }

    synchronizer = OAISynchronizer(migrate_provider, parser_name="test_parser",
                                   create_record=create_handler)
    synchronizer.sickle.GetRecord = MagicMock(return_value=Record())
    synchronizer.transformer.transform = MagicMock(return_value={
        "id": "1",
        "title": "Some title",
        "language": ["cze", "eng"]
    })
    synchronizer.oai_sync = OAISync(provider_id=migrate_provider.id)
    synchronizer.update("bla", datetime.utcnow())


def test_get_oai_identifiers(migrate_provider):
    oai_sync = OAISynchronizer(migrate_provider)
    results = oai_sync._get_oai_identifiers()
    assert isinstance(results, OAIItemIterator)


def test_get_oai_identifiers_2(migrate_provider):
    oai_sync = OAISynchronizer(migrate_provider)
    results = oai_sync._get_oai_identifiers(
        sickle=Sickle("https://invenio.nusl.cz/oai2d/"),
        metadata_prefix="marcxml",
    )
    assert isinstance(results, OAIItemIterator)

# import pytest
#
# from invenio_oarepo_oai_pmh_harvester.models import OAIProvider
# from invenio_oarepo_oai_pmh_harvester.synchronization import OAISynchronizer
#
#
# def test_synchronization_instance(app, db, unhandled_paths):
#     provider = OAIProvider.query.filter_by(code="uk").one_or_none()
#     if not provider:
#         provider = OAIProvider(
#             code="uk",
#             oai_endpoint="https://dspace.cuni.cz/oai/nusl",
#             set_="nusl_set",
#             metadata_prefix="xoai",
#             constant_fields={
#                 "provider": {
#                     "$ref": "https://localhost:5000/api/taxonomies/institutions/00216208"
#                 },
#                 "accessRights": {
#                     "$ref": "https://localhost:5000/api/taxonomies/accessRights/c_abf2"
#                 },
#                 "accessibility": [
#                     {
#                         "value": "Dostupné v digitálním repozitáři UK.",
#                         "lang": "cze"
#                     },
#                     {
#                         "value": "Available in the Charles University Digital Repository.",
#                         "lang": "eng"
#                     }
#                 ]
#             }
#         )
#         db.session.add(provider)
#         db.session.commit()
#     synchronizer = OAISynchronizer(provider, 'xoai', unhandled_paths=unhandled_paths)
#     print(synchronizer)
#     synchronizer.run()
#
#
# @pytest.fixture()
# def unhandled_paths():
#     return {
#         "/dc/date/accessioned",
#         "/dc/date/available",
#         "/dc/date/issued",
#         "/dc/identifier/repId",
#         "/dc/identifier/aleph",
#         "/dc/description/provenance",
#         "/dc/description/department",
#         "/dc/description/faculty",
#         "/dc/language/cs_CZ",
#         "/dc/publisher",
#         "/dcterms/created",
#         "/thesis/degree/name",
#         "/thesis/degree/program",
#         "/thesis/degree/level",
#         "/uk/abstract",
#         "/uk/thesis",
#         "/uk/taxonomy",
#         "/uk/faculty-name",
#         "/uk/faculty-abbr",
#         "/uk/degree-discipline",
#         "/uk/degree-program",
#         "/uk/publication-place",
#         "/bundles",
#         "/others/handle",
#         "/others/lastModifyDate",
#         "/repository"
#     }

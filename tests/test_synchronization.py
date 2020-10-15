from oarepo_oai_pmh_harvester.ext import OArepoOAIClient
from oarepo_oai_pmh_harvester.proxies import current_oai_client


def test_get_endpoint_config(app, db, metadata):
    client = OArepoOAIClient(app)
    synchronizer = current_oai_client.synchronizers["uk"]
    res = synchronizer.get_endpoint_config(metadata)
    assert res is not None
    assert isinstance(res, dict)


def test_create_record(app, db, metadata):
    client = OArepoOAIClient(app)
    synchronizers = current_oai_client.synchronizers
    synchronizer = synchronizers["uk"]
    rec = synchronizer.create_record(metadata)
    print(rec)

# import random
# from datetime import datetime
# from pprint import pprint
# from unittest.mock import MagicMock
#
# import pytest
# from requests import ConnectionError
# from sickle import Sickle
# from sickle.iterator import OAIItemIterator
#
# from oarepo_oai_pmh_harvester.exceptions import HandlerNotFoundError
# from oarepo_oai_pmh_harvester.models import OAISync
# from oarepo_oai_pmh_harvester.synchronization import OAISynchronizer
#
#
# def test_init(app, test_db, migrate_provider):
#     synchronizer = OAISynchronizer(migrate_provider)
#     assert synchronizer is not None
#
#
# def test_delete(migrate_provider):
#     def delete_handler(oai_identifier):
#         pass
#
#     synchronizer = OAISynchronizer(migrate_provider, delete_record=delete_handler)
#     synchronizer.delete("bla")
#
#
# def test_delete_2(migrate_provider):
#     synchronizer = OAISynchronizer(migrate_provider)
#     with pytest.raises(HandlerNotFoundError):
#         synchronizer.delete("bla")
#
#
# def test_synchronize_delete(migrate_provider):
#     def delete_handler(oai_identifier, datestamp):
#         print("deleted")
#
#     class Identifier:
#         datestamp = datetime.utcnow()
#         identifier = random.randint(0, 100000)
#         deleted = True
#
#     identifiers = [Identifier() for x in range(10)]
#     synchronizer = OAISynchronizer(migrate_provider, delete_record=delete_handler)
#     synchronizer.synchronize(identifiers=identifiers)
#     assert synchronizer.deleted == 10
#
#
# def test_synchronize_create(migrate_provider, record_xml, sample_record):
#     class Record:
#         xml = record_xml
#
#     def create_handler(*args, **kwargs):
#         return sample_record
#
#     @Decorators.parser("test_parser", "nusl")
#     def parser(*args, **kwargs):
#         return {
#             "id": "1",
#             "title": "Some title",
#             "language": ["cze", "eng"]
#         }
#
#     synchronizer = OAISynchronizer(migrate_provider,
#                                    parser_name="test_parser",
#                                    create_record=create_handler,
#                                    id_handler=nusl_theses.attach_id
#                                    )
#     synchronizer.sickle.GetRecord = MagicMock(return_value=Record())
#     synchronizer.transformer.transform = MagicMock(return_value={
#         "id": "1",
#         "title": "Some title",
#         "language": ["cze", "eng"]
#     })
#     synchronizer.oai_sync = OAISync(provider_id=migrate_provider.id)
#     record = synchronizer.create_or_update("bla", datetime.utcnow())
#     assert record == {'id': '1', 'identifier': [{'value': 'oai:server:id', 'type':
#     'originalOAI'}]}
#
#
# def test_get_oai_identifiers(migrate_provider):
#     oai_sync = OAISynchronizer(migrate_provider)
#     try:
#         results = oai_sync._get_oai_identifiers()
#         assert isinstance(results, OAIItemIterator)
#     except ConnectionError:
#         pytest.skip("Connection error")
#
#
# def test_get_oai_identifiers_2(migrate_provider):
#     oai_sync = OAISynchronizer(migrate_provider)
#     try:
#         results = oai_sync._get_oai_identifiers(
#             sickle=Sickle("https://invenio.nusl.cz/oai2d/"),
#             metadata_prefix="marcxml",
#         )
#         assert isinstance(results, OAIItemIterator)
#     except ConnectionError:
#         pytest.skip("Connection error")

import json
import pathlib

from invenio_oarepo_oai_pmh_harvester.rules_ import Rules
from invenio_oarepo_oai_pmh_harvester.transformer import OAITransformer
from tests.uk import UK


def test_unhandled_paths():
    class Handlers(Rules):
        pass

    record = {
        "dc": {
            "date": {
                "accessioned": "bla",
                "available": "bla"
            }
        }
    }
    unhandled_paths = {"/dc/date/accessioned", "/dc/date/available"}
    transformer = OAITransformer(Handlers(), unhandled_paths=unhandled_paths)
    transformer.transform(record)

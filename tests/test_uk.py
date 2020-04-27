import json
from pathlib import Path
from pprint import pprint

from invenio_oarepo_oai_pmh_harvester.transformer import OAITransformer
from tests.uk import UK


def test_simple(app, db):
    unhandled_paths = {
        "/dc/date/accessioned",
        "/dc/date/available",
        "/dc/date/issued",
        "/dc/identifier/repId",
        "/dc/identifier/aleph",
        "/dc/description/provenance",
        "/dc/description/department",
        "/dc/description/faculty",
        "/dc/language/cs_CZ",
        "/dc/publisher",
        "/dcterms/created",
        "/thesis/degree/name",
        "/thesis/degree/program",
        "/thesis/degree/level",
        "/uk/thesis",
        "/uk/taxonomy",
        "/uk/faculty-name",
        "/uk/faculty-abbr",
        "/uk/degree-discipline",
        "/uk/degree-program",
        "/uk/publication-place",
        "/bundles",
        "/others/handle",
        "/others/lastModifyDate",
        "/repository"
    }
    transformer = OAITransformer(UK(), unhandled_paths=unhandled_paths)

    with open(Path(__file__).parent / "data/sample.json") as f:
        json_sample = json.load(f)
    tranformed = transformer.transform(json_sample)
    print("\n\n")
    print("TRANSFORMED")
    pprint(tranformed)
    print("\n\n")

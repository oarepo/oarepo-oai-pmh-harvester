import json
from pathlib import Path
from pprint import pprint

from invenio_oarepo_oai_pmh_harvester.transformer import OAITransformer
from tests.uk import UK


def test_simple(app, db):
    transformer = OAITransformer(UK())

    with open(Path(__file__).parent / "data/sample.json") as f:
        json_sample = json.load(f)
    tranformed = transformer.transform(json_sample)
    print("\n\n")
    print("TRANSFORMED")
    pprint(tranformed)
    print("\n\n")

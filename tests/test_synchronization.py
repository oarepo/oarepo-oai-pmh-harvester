import json
from pprint import pprint

from invenio_db import db

from invenio_oarepo_oai_pmh_harvester.models import OAIProvider
from invenio_oarepo_oai_pmh_harvester.s_parser import xml_to_dict_xoai, parser_refine
from invenio_oarepo_oai_pmh_harvester.synchronization import OAISynchronizer


def test_synchronization_instance(app, test_db):
    provider = OAIProvider(
        code="uk",
        oai_endpoint="https://dspace.cuni.cz/oai/nusl",
        set_="nusl_set",
        metadata_prefix="xoai"
    )
    db.session.add(provider)
    db.session.commit()
    synchronizer = OAISynchronizer(provider)
    synchronizer.run()


def test_transform(app, test_db, synchronizer_instance, record_xml):
    result = synchronizer_instance.parse(record_xml, parser=parser_refine)
    print(result)
    with open("/tmp/uk.json", "w") as f:
        json.dump(result,f, ensure_ascii=False)
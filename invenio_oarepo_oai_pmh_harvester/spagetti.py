from pprint import pprint

from sickle import Sickle

from invenio_oarepo_oai_pmh_harvester.s_parser import xml_to_dict_xoai

sickle = Sickle(endpoint="https://dspace.cuni.cz/oai/nusl")
records = sickle.ListRecords(metadataPrefix='xoai', set='nusl_set')

for record in records:
    # tree_dict = xml_to_dict_xoai(record.xml)
    with open("/tmp/test_xml.xml", "w") as f:
        f.write(record.raw)
    print("done")

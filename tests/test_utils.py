from sickle.models import Header

from oarepo_oai_pmh_harvester.utils import get_oai_header_data


def test_get_oai_header_data(load_entry_points, app, db, record_xml):
    header_xml = record_xml[0]
    header = Header(header_xml)
    res_tuple = get_oai_header_data(header)
    assert res_tuple == ('2017-09-11T08:12:53Z', False, 'oai:dspace.cuni.cz:20.500.11956/2623')


def test_get_oai_header_data_2(load_entry_points, app, db, record_xml):
    res_tuple = get_oai_header_data(xml=record_xml)
    assert res_tuple == ('2017-09-11T08:12:53Z', False, 'oai:dspace.cuni.cz:20.500.11956/2623')
from collections import defaultdict

from lxml.etree import _Element
from sickle.models import Header
from sickle.utils import get_namespace


def infinite_dd():
    return defaultdict(infinite_dd)


def get_oai_header_data(header: Header = None, xml: _Element = None):
    if not (header or xml):
        raise Exception("Must provide header or xml")
    if header and xml:
        raise Exception("You must provide only header or xml")
    if xml:
        header = Header(xml.find('.//' + get_namespace(xml) + 'header'))
    datestamp = header.datestamp
    oai_identifier = header.identifier
    deleted = header.deleted
    return datestamp, deleted, oai_identifier
from collections import defaultdict

from lxml.etree import _Element
from sickle.models import Header
from sickle.utils import get_namespace


def infinite_dd():
    return defaultdict(infinite_dd)


def get_oai_header_data(header: Header = None, xml: _Element = None):
    if not (header or xml):  # pragma: no cover
        raise Exception("Must provide header or xml")
    if header and xml:  # pragma: no cover
        raise Exception("You must provide only header or xml")
    if xml:
        header = Header(xml.find('.//' + get_namespace(xml) + 'header'))
    datestamp = header.datestamp
    oai_identifier = header.identifier
    deleted = header.deleted
    return datestamp, deleted, oai_identifier


def merge(a, b, path=None):
    "merges b into a"
    if path is None: path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge(a[key], b[key], path + [str(key)])
            elif a[key] == b[key]:
                pass  # same leaf value
            elif isinstance(a[key], list) and isinstance(b[key], list):
                for _ in b[key]:
                    if _ not in a[key]:
                        a[key].append(_)
            elif isinstance(a[key], str) and isinstance(b[key], str):
                a[key] = [a[key], b[key]]
            elif isinstance(a[key], list) and isinstance(b[key], str):
                if b[key] not in a[key]:
                    a[key].append(b[key])
            else:
                raise Exception('Conflict at %s' % '.'.join(path + [str(key)]))
        else:
            a[key] = b[key]
    return a

def transform_to_dict(source):
    if isinstance(source, (dict, defaultdict)):
        target = {}
        for k, v in source.items():
            target[k] = transform_to_dict(v)
    elif isinstance(source, (list, tuple)):
        target = []
        for _ in source:
            target.append(transform_to_dict(_))
    else:
        target = source
    return target
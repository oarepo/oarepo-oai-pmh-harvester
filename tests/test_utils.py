import jmespath
from pytest import fixture

from invenio_oarepo_oai_pmh_harvester.utils import add_node, update_node


@fixture
def nested_dict():
    return {
        'dc': {
            'contributor': {
                'advisor': {'none': {'field': set()}}, 'referee': {'none': {'field': set()}}
            }, 'creator': {'none': {'field': set()}}, 'date': {
                'accessioned': {'none': {'field': set()}}, 'available': {'none': {'field': set()}},
                'issued': {'none': {'field': set()}}
            }, 'identifier': {
                'uri': {'none': {'field': set()}}, 'repId': {'none': {'field': set()}},
                'aleph': {'none': {'field': set()}}
            }, 'description': {
                'abstract': {'cs_CZ': {'field': set()}, 'en_US': {'field': set()}},
                'provenance': {'en': {'field': set()}}, 'department': {'cs_CZ': {'field': set()}},
                'faculty': {'en_US': {'field': set()}, 'cs_CZ': {'field': set()}}
            }, 'language': {'cs_CZ': {'field': set()}, 'iso': {'none': {'field': set()}}},
            'publisher': {'cs_CZ': {'field': set()}},
            'title': {'cs_CZ': {'field': set()}, 'translated': {'en_US': {'field': set()}}},
            'type': {'cs_CZ': {'field': set()}}
        }, 'dcterms': {
            'created': {'none': {'field': set()}}, 'dateAccepted': {'none': {'field': set()}}
        }, 'thesis': {
            'degree': {
                'name': {'none': {'field': set()}}, 'level': {'cs_CZ': {'field': set()}},
                'discipline': {'en_US': {'field': set()}, 'cs_CZ': {'field': set()}},
                'program': {'en_US': {'field': set()}, 'cs_CZ': {'field': set()}}
            }, 'grade': {'cs': {'cs_CZ': {'field': set()}}, 'en': {'en_US': {'field': set()}}}
        }, 'uk': {
            'thesis': {'type': {'cs_CZ': {'field': set()}}},
            'taxonomy': {'organization-cs': {'cs_CZ': {'field': set()}}},
            'faculty-name': {'cs': {'cs_CZ': {'field': set()}}, 'en': {'en_US': {'field': set()}}},
            'faculty-abbr': {'cs': {'cs_CZ': {'field': set()}}}, 'degree-discipline': {
                'cs': {'cs_CZ': {'field': set()}}, 'en': {'en_US': {'field': set()}}
            }, 'degree-program': {
                'cs': {'cs_CZ': {'field': set()}}, 'en': {'en_US': {'field': set()}}
            }, 'abstract': {'cs': {'cs_CZ': {'field': set()}}, 'en': {'en_US': {'field': set()}}},
            'publication-place': {'cs_CZ': {'field': set()}}, 'grantor': {'cs_CZ': {'field': set()}}
        }, 'bundles': {'bundle': {'bitstreams': {'bitstream': {'field': set()}}}},
        'others': {'field': set()}, 'repository': {'field': set()}
    }


def test_address():
    address = 'dc.contributor.advisor.none'
    assert add_node(address, "field") == 'dc.contributor.advisor.none.field'


def test_update_node(nested_dict):
    new_dict = update_node('dc.contributor.advisor.none.field', nested_dict, ["Kopecký, Daniel"])
    new_value = jmespath.search("dc.contributor.advisor.none.field", new_dict)
    assert new_value == {"Kopecký, Daniel"}

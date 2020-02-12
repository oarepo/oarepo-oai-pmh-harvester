import jmespath

from invenio_oarepo_oai_pmh_harvester.utils import sanitize_address


def test_sanitize_address_1():
    expression = "uk.taxonomy.organization-cs"
    new_expression = sanitize_address(expression)
    slovnik = {
        "uk": {
            "taxonomy": {
                "organization-cs": "test_passed"
            }
        }
    }
    node = jmespath.search(new_expression, slovnik)
    assert node == "test_passed"


def test_sanitize_address_2():
    expression = "uk.taxonomy.@organization-cs"
    new_expression = sanitize_address(expression)
    slovnik = {
        "uk": {
            "taxonomy": {
                "@organization-cs": "test_passed"
            }
        }
    }
    node = jmespath.search(new_expression, slovnik)
    assert node == "test_passed"
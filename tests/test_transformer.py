import pytest

from invenio_oarepo_oai_pmh_harvester.transformer import OAITransformer


def test_init():
    transformer = OAITransformer(rules={}, unhandled_paths=set("/path/to/field"))
    assert transformer.rules == {}
    assert transformer.unhandled_paths == set("/path/to/field")


def test_init_2():
    transformer = OAITransformer()
    assert transformer.rules == {}
    assert transformer.unhandled_paths == set()


def test_iter_json_1():
    def transform_handler(paths, el, results, phase, **kwargs):
        results[0]["spam"] = el
        return OAITransformer.PROCESSED

    record = {
        "path": {
            "to": {
                "field": "bla"
            }
        },
        "spam": "ham"
    }
    rules = {
        "/spam": {
            "pre": transform_handler
        }
    }
    transformer = OAITransformer(rules=rules, unhandled_paths={"/path/to/field", })
    result = transformer.transform(record)
    assert result == {"spam": "ham"}


def test_iter_json_2():
    def transform_handler(paths, el, results, phase, **kwargs):
        results[-1].setdefault("spam", [])
        results[-1]["spam"].append(el)
        return OAITransformer.PROCESSED

    record = {
        "path": {
            "to": {
                "field": "bla"
            }
        },
        "spam": ["ham", "blabla"]
    }
    rules = {
        "/spam": {
            "pre": transform_handler
        }
    }
    transformer = OAITransformer(rules=rules, unhandled_paths={"/path/to/field", })
    result = transformer.transform(record)
    assert result == {"spam": ["ham", "blabla"]}


def test_iter_json_3():
    def transform_handler(paths, el, results, phase, **kwargs):
        results[0]["spam"] = el
        return OAITransformer.PROCESSED

    record = {
        "path": {
            "to": {
                "field": "bla"
            }
        },
        "spam": "ham"
    }
    rules = {
        "/spam": {
            "pre": transform_handler
        }
    }
    transformer = OAITransformer(rules=rules)
    with pytest.raises(ValueError):
        transformer.transform(record)


def test_iter_json_4():
    def transform_handler(paths, el, results, phase, **kwargs):
        results[0]["spam"] = el
        return OAITransformer.PROCESSED

    record = {
        "path": {
            "to": {
                "field": "bla"
            }
        },
        "spam": [
            {
                "ham": "blabla",
            },
            {
                "unhandled_option": ["nothing"]
            }
        ]
    }
    rules = {
        "/spam/ham": {
            "pre": transform_handler
        }
    }
    transformer = OAITransformer(rules=rules, unhandled_paths={"/path/to/field", })
    with pytest.raises(ValueError):
        result = transformer.transform(record)

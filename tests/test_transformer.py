from pprint import pprint

import pytest

from oarepo_oai_pmh_harvester.transformer import OAITransformer


class TestTransformer:
    def test_init(self):
        transformer = OAITransformer(rules={}, unhandled_paths=set("/path/to/field"))
        assert transformer.rules == {}
        assert transformer.unhandled_paths == set("/path/to/field")

    def test_init_2(self):
        transformer = OAITransformer()
        assert transformer.rules == {}
        assert transformer.unhandled_paths == set()

    def test_iter_json_1(self):
        def transform_handler(el, **kwargs):
            return {"spam": el}

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

    def test_iter_json_2(self):
        def transform_handler(el, **kwargs):
            return {"spam": el}

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

    def test_iter_json_3(self):
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

    def test_iter_json_4(self):
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

    def test_iter_json_5(self):
        def transform_handler(el, **kwargs):
            return {
                "spam": {
                    "spam1": el
                }
            }

        def transform_handler_2(el, **kwargs):
            return {
                "spam": {
                    "spam2": el
                }
            }

        record = {
            "path": {
                "to": {
                    "field": "bla"
                }
            },
            "spam": "ham",
            "spam2": "blah"
        }
        rules = {
            "/spam": {
                "pre": transform_handler
            },
            "/spam2": {
                "pre": transform_handler_2
            }
        }
        transformer = OAITransformer(rules=rules, unhandled_paths={"/path/to/field", })
        result = transformer.transform(record)
        assert result == {'spam': {'spam1': 'ham', 'spam2': 'blah'}}

    def test_iter_json_6(self):
        def transform_handler(el, **kwargs):
            return {
                "spam": {
                    "spam1": el
                }
            }

        def transform_handler_2(el, **kwargs):
            raise Exception("Test exception")

        record = {
            "path": {
                "to": {
                    "field": "bla"
                }
            },
            "spam": "ham",
            "spam2": "blah"
        }
        rules = {
            "/spam": {
                "pre": transform_handler
            },
            "/spam2": {
                "pre": transform_handler_2
            }
        }
        transformer = OAITransformer(rules=rules, unhandled_paths={"/path/to/field", })
        result = transformer.transform(record)
        rulesExceptions = result["rulesExceptions"]
        assert rulesExceptions is not None
        assert "path" in rulesExceptions[0]
        assert "phase" in rulesExceptions[0]
        assert "exception" in rulesExceptions[0]
        del result["rulesExceptions"]
        assert result == {
            'spam': {'spam1': 'ham'}
        }

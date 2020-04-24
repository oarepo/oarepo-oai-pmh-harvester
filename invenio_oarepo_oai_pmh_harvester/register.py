import functools

from pkg_resources import iter_entry_points

from invenio_oarepo_oai_pmh_harvester.transformer import OAITransformer
from invenio_oarepo_oai_pmh_harvester.utils import infinite_dd


class Singleton:
    __instance = None

    def __new__(cls, val=None):
        if Singleton.__instance is None:
            Singleton.__instance = object.__new__(cls)
        return Singleton.__instance


class Registry(Singleton):
    def __init__(self):
        self.parsers_ep = "invenio_oarepo_oai_pmh_harvester.parsers"
        self.rules_ep = "invenio_oarepo_oai_pmh_harvester.rules"
        self.parsers = infinite_dd()
        self.rules = infinite_dd()

    def get_parsers(self):
        for ep in iter_entry_points(group=self.parsers_ep):
            ep.load()

    def get_rules(self):
        for ep in iter_entry_points(group=self.rules_ep):
            ep.load()

    def add_parser(self, func, name, provider):
        self.parsers[provider][name] = func

    def add_rule(self, func, target_field_name, provider):
        self.rules[provider][target_field_name] = func


registry = Registry()


class Decorators:
    @staticmethod
    def parser(name, provider):
        def real_decorator(func):
            registry.add_parser(func, name, provider)

        return real_decorator

    @staticmethod
    def pre_rule(path):
        def wrapper(func):
            func._transform_path = path
            func._transform_phase = OAITransformer.PHASE_PRE
            return func

        return wrapper

    @staticmethod
    def post_rule(path):
        def wrapper(func):
            func._transform_path = path
            func._transform_phase = OAITransformer.PHASE_POST
            return func

        return wrapper

    @staticmethod
    def array_value(func):
        @functools.wraps(func)
        def wrapped(**kwargs):
            ret = func(**kwargs)
            if isinstance(ret, list):
                kwargs["results"][-1].extend(ret)
            else:
                kwargs["results"][-1].append(ret)
            return OAITransformer.PROCESSED

        return wrapped

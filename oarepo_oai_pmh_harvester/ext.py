from collections import defaultdict

from invenio_db import db
from pkg_resources import iter_entry_points

from oarepo_oai_pmh_harvester.transformer import OAITransformer
from oarepo_oai_pmh_harvester.utils import infinite_dd
from . import config
from .models import OAIProvider
from .synchronization import OAISynchronizer


class Singleton(type):
    _instances = {}

    # Rewritten type() method, where built_in type method has this signature "type(name, bases,
    # dict)"
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class OArepoOAIClientState(metaclass=Singleton):
    def __init__(self, app, _rules: defaultdict = None, _parsers: defaultdict = None,
                 _providers: dict = None, _synchronizers=None, transformer_class=OAITransformer,
                 _endpoints=None):
        self.app = app
        self._rules = _rules
        self._parsers = _parsers
        self._providers = _providers
        self._synchronizers = _synchronizers
        self.transformer_class = transformer_class
        self._endpoints = _endpoints
        print(self.endpoints)

    @property
    def providers(self):
        if self._providers is None:
            self.create_providers()
        return self._providers

    @property
    def rules(self):
        if self._rules is None:
            self._load_rules()
        return self._rules

    @property
    def parsers(self):
        if self._parsers is None:
            self._load_parsers()
        return self._parsers

    @property
    def synchronizers(self):
        if not self._synchronizers:
            self.load_synchronizers()
        return self._synchronizers

    @property
    def endpoints(self):
        if not self._endpoints:
            self.load_endpoints()
        return self._endpoints

    def load_endpoints(self):
        self._endpoints = self.app.config.get("RECORDS_REST_ENDPOINTS", {})

    def _load_rules(self):
        for ep in iter_entry_points('oarepo_oai_pmh_harvester.rules'):
            ep.load()

    def _load_parsers(self):
        for ep in iter_entry_points('oarepo_oai_pmh_harvester.parsers'):
            ep.load()

    def create_providers(self):
        providers = self.app.config.get("OAREPO_OAI_PROVIDERS")
        if providers:
            for k, v in providers.items():
                provider = OAIProvider.query.filter_by(code=k).one_or_none()
                if provider:
                    continue
                provider = OAIProvider(
                    code=k,
                    description=v.get("description"),
                    oai_endpoint=v.get("oai_endpoint"),
                    set_=v.get("set"),
                    metadata_prefix=v.get("metadata_prefix"),
                    constant_fields=v.get("constant_fields", {}),
                    unhandled_paths=v.get("unhandled_paths", []),
                    default_endpoint=v.get("default_endpoint"),
                    endpoint_mapping=v.get("endpoint_mapping")
                )
                if not self._providers:
                    self._providers = {}
                self._providers.setdefault(k, provider)
                db.session.add(provider)
            db.session.commit()

    def rule(self, path, parser, phase=OAITransformer.PHASE_PRE):
        def wrapper(func):
            self.add_rule(func, parser, path, phase)

        return wrapper

    def parser(self, name, provider):
        def wrapper(func):
            self.add_parser(func, name, provider)

        return wrapper

    def add_rule(self, func, parser_name, path, phase):
        if not self._rules:
            self._rules = infinite_dd()
        self._rules[parser_name][path][phase] = func

    def add_parser(self, func, name, provider):
        if not self._parsers:
            self._parsers = infinite_dd()
        self._parsers[provider][name] = func

    def load_synchronizers(self):
        providers = self.providers
        if not providers:
            raise Exception("No providers, please provide provider in config")
        for k, provider in self._providers.items():
            if not self._synchronizers:
                self._synchronizers = {}
            self._synchronizers.setdefault(k, OAISynchronizer(
                provider=provider,
                parser=self.parsers[k][provider.metadata_prefix],
                transformer=self.transformer_class(
                    rules=self.rules[provider.metadata_prefix],
                    unhandled_paths=set(provider.unhandled_paths)),
                endpoints=self.endpoints,
                default_endpoint=provider.default_endpoint,
                endpoint_mapping=provider.endpoint_mapping

            )
                                           )
        print(self._synchronizers)

    def run(self):
        # TODO:
        """
        Function that start OAI synchronization
        """
        for k, v in self.synchronizers.items():
            v.run()


class OArepoOAIClient:

    def __init__(self, app=None):
        """Extension initialization."""
        if app:
            self.init_app(app)

    def init_app(self, app):
        self.init_config(app)
        app.extensions['oarepo-oai-client'] = OArepoOAIClientState(app)

    def init_config(self, app):
        for k in dir(config):
            if k.startswith('OAREPO_OAI_'):
                app.config.setdefault(k, getattr(config, k))

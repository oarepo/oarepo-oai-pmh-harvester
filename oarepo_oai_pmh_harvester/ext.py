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
        # TODO: dodělat kontrolu jestli je v DB
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
                )
                db.session.add(provider)
                db.session.commit()
                provider._synchronizers = {}
                for sync_config in v.get("synchronizers", []):
                    synchronizer = self.create_synchronizer(provider.code, sync_config, provider.id)
                    provider._synchronizers[sync_config["name"]] = synchronizer
                if not self._providers:
                    self._providers = {}
                self._providers.setdefault(k, provider)
            db.session.commit()

    def rule(self, provider, parser, path, phase=OAITransformer.PHASE_PRE):
        def wrapper(func):
            self.add_rule(func, provider, parser, path, phase)

        return wrapper

    def parser(self, name, provider):
        def wrapper(func):
            self.add_parser(func, name, provider)

        return wrapper

    def add_rule(self, func, provider, parser_name, path, phase):
        if not self._rules:
            self._rules = infinite_dd()
        self._rules[provider][parser_name][path][phase] = func

    def add_parser(self, func, name, provider):
        if not self._parsers:
            self._parsers = infinite_dd()
        self._parsers[provider][name] = func

    def create_synchronizer(self, provider_code, config, provider_id):
        return OAISynchronizer(
            provider_id=provider_id,
            metadata_prefix=config["metadata_prefix"],
            set_=config["set"],
            constant_fields=config.get("constant_field", {}),
            oai_endpoint=config["oai_endpoint"],
            parser=self.parsers[provider_code][config["metadata_prefix"]],
            transformer=self.transformer_class(
                rules=self.rules[provider_code][config["metadata_prefix"]],
                unhandled_paths=set(config.get("unhandled_paths", []))),
            endpoints=self.endpoints,
            default_endpoint=config.get("default_endpoint", "recid"),
            endpoint_mapping=config.get("endpoint_mapping", {})
        )


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

from collections import defaultdict
from typing import List, Union

from pkg_resources import iter_entry_points

from oarepo_oai_pmh_harvester.transformer import OAITransformer
from oarepo_oai_pmh_harvester.utils import infinite_dd
from . import config
from .provider import OAIProvider
from .synchronization import OAISynchronizer
from .views import oai_client_blueprint


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
                 _endpoints=None, endpoint_handlers: dict = None, _pre_processors: dict = None,
                 _post_processors: dict = None):
        self.app = app
        self._rules = _rules
        self._parsers = _parsers
        self._endpoint_handlers = endpoint_handlers
        self._providers = _providers
        self._synchronizers = _synchronizers
        self.transformer_class = transformer_class
        self._endpoints = _endpoints
        self._pre_processors = _pre_processors
        self._post_processors = _post_processors
        self.es_index = None

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
    def endpoints(self):
        if not self._endpoints:
            self.load_endpoints()
        return self._endpoints

    @property
    def endpoint_handlers(self):
        if self._endpoint_handlers is None:
            self._load_endpoint_handlers()
        return self._endpoint_handlers

    @property
    def pre_processors(self):
        if self._pre_processors is None:
            self._load_pre_processors()
        return self._pre_processors

    @property
    def post_processors(self):
        if self._post_processors is None:
            self._load_post_processors()
        return self._post_processors

    def load_endpoints(self):
        res = {}
        draft_endpoints = self.app.config.get("RECORDS_DRAFT_ENDPOINTS")
        if draft_endpoints:
            res.update(self.app.config["RECORDS_REST_ENDPOINTS"].endpoints)
        else:
            res.update(self.app.config.get("RECORDS_REST_ENDPOINTS", {}))
        self._endpoints = res

    def _load_rules(self):
        for ep in iter_entry_points('oarepo_oai_pmh_harvester.rules'):
            ep.load()

    def _load_parsers(self):
        for ep in iter_entry_points('oarepo_oai_pmh_harvester.parsers'):
            ep.load()

    def _load_endpoint_handlers(self):
        for ep in iter_entry_points('oarepo_oai_pmh_harvester.mappings'):
            ep.load()

    def _load_pre_processors(self):
        for ep in iter_entry_points('oarepo_oai_pmh_harvester.pre_processors'):
            ep.load()

    def _load_post_processors(self):
        for ep in iter_entry_points('oarepo_oai_pmh_harvester.post_processors'):
            ep.load()

    def create_providers(self):
        providers = self.app.config.get("OAREPO_OAI_PROVIDERS")
        if providers:
            for k, v in providers.items():
                provider = OAIProvider(
                    code=k,
                    description=v.get("description"),
                )  # vytvořím providera
                provider.synchronizers = {}
                for sync_config in v.get("synchronizers", []):
                    synchronizer = self.create_synchronizer(provider.code, sync_config)
                    provider.synchronizers[sync_config["name"]] = synchronizer
                if not self._providers:
                    self._providers = {}
                self._providers.setdefault(k, provider)

    def add_rule(self, func, provider, parser_name, path, phase):
        if not self._rules:
            self._rules = infinite_dd()
        self._rules[provider][parser_name][path][phase] = func

    def add_parser(self, func, name):
        if not self._parsers:
            self._parsers = infinite_dd()
        self._parsers[name] = func

    def add_endpoint_handler(self, func, provider, parser_name):
        if not self._endpoint_handlers:
            self._endpoint_handlers = infinite_dd()
        self._endpoint_handlers[provider][parser_name] = func

    def add_pre_processor(self, func, provider, parser_name):
        if not self._pre_processors:
            self._pre_processors = defaultdict(lambda: defaultdict(list))
        self._pre_processors[provider][parser_name].append(func)

    def add_post_processor(self, func, provider, parser_name):
        if not self._post_processors:
            self._post_processors = defaultdict(lambda: defaultdict(list))
        self._post_processors[provider][parser_name].append(func)

    def create_synchronizer(self, provider_code, config):
        return OAISynchronizer(
            name=config["name"],
            provider_code=provider_code,
            metadata_prefix=config["metadata_prefix"],
            set_=config["set"],
            constant_fields=config.get("constant_field", {}),
            oai_endpoint=config["oai_endpoint"],
            parser=self.parsers[config["metadata_prefix"]],
            transformer=self.transformer_class(
                rules=self.rules[provider_code][config["metadata_prefix"]],
                unhandled_paths=set(config.get("unhandled_paths", []))),
            endpoints=self.endpoints,
            default_endpoint=config.get("default_endpoint", "recid"),
            endpoint_mapping=config.get("endpoint_mapping", {}),
            from_=config.get("from"),
            endpoint_handler=self.endpoint_handlers,
            bulk=config.get("bulk", True),
            pre_processors=self.pre_processors[provider_code][
                config["metadata_prefix"]] if self.pre_processors else None,
            post_processors=self.post_processors[provider_code][
                config["metadata_prefix"]] if self.post_processors else None
        )

    def run(self, providers_codes: List[str] = None, synchronizers_codes: List[str] = None,
            break_on_error: bool = True, start_oai: str = None,
            start_id: int = 0, overwrite: bool = False, only_fetch: bool = False):
        if not providers_codes:
            providers_codes = [_ for _ in self.providers.keys()]
        if len(providers_codes) > 1:
            for code in providers_codes:
                self._run_provider(code, break_on_error=break_on_error, only_fetch=only_fetch)
        elif len(providers_codes) == 1:
            if not synchronizers_codes:
                synchronizers_codes = [_ for _ in
                                       self.providers[providers_codes[0]].synchronizers.keys()]
            if len(synchronizers_codes) > 1:
                for code in synchronizers_codes:
                    self._run_synchronizer(providers_codes[0], code, break_on_error=break_on_error,
                                           only_fetch=only_fetch)
            elif len(synchronizers_codes) == 1:
                if start_oai and start_id != 0:
                    raise Exception("You can not enter start_oai and START_ID simultaneously.")
                elif start_oai:
                    self._run_synchronizer(providers_codes[0], synchronizers_codes[0],
                                           break_on_error=break_on_error, start_oai=start_oai,
                                           only_fetch=only_fetch)
                elif start_id != 0:
                    self._run_synchronizer(providers_codes[0], synchronizers_codes[0],
                                           break_on_error=break_on_error, start_id=start_id,
                                           only_fetch=only_fetch)
                else:
                    self._run_synchronizer(providers_codes[0], synchronizers_codes[0],
                                           break_on_error=break_on_error, only_fetch=only_fetch)
            else:
                raise Exception("Something unexpected happened.")
        else:
            raise Exception("Something unexpected happened.")

    def _run_provider(self, provider: str, break_on_error: bool = True, overwrite: bool = False,
                      only_fetch: bool = False):
        provider_ = self.providers[provider]
        for synchronizer in provider_.synchronizers.keys():
            self._run_synchronizer(provider, synchronizer, break_on_error=break_on_error,
                                   overwrite=overwrite, only_fetch=only_fetch)

    def _run_synchronizer(self, provider: str, synchronizer: str, start_oai: str = None,
                          start_id: int = 0, break_on_error: bool = True, overwrite: bool = False,
                          only_fetch: bool = False):
        provider = self.providers[provider]
        synchronizer = provider.synchronizers[synchronizer]
        synchronizer.run(start_oai=start_oai, start_id=start_id, break_on_error=break_on_error,
                         overwrite=overwrite, only_fetch=only_fetch, index=self.es_index)

    def run_synchronizer_by_ids(self,
                                oai_id: Union[str, List[str]],
                                provider: str,
                                synchronizer: str,
                                break_on_error: bool = True,
                                overwrite: bool = False,
                                bulk: bool = False,
                                only_fetch: bool = False
                                ):
        provider = self.providers[provider]
        synchronizer = provider.synchronizers[synchronizer]
        synchronizer.bulk = bulk
        synchronizer.run(break_on_error=break_on_error, oai_id=oai_id, overwrite=overwrite,
                         only_fetch=only_fetch)


class OArepoOAIClient:

    def __init__(self, app=None):
        """Extension initialization."""
        if app:
            self.init_app(app)

    def init_app(self, app):
        self.init_config(app)

        # register blueprint
        prefix = app.config.get('OAREPO_OAI_CLIENT_URL_PREFIX', "/oai-client")
        if prefix.startswith('/api'):
            prefix = prefix[4:]
        app.register_blueprint(oai_client_blueprint, url_prefix=prefix)

        app.extensions['oarepo-oai-client'] = OArepoOAIClientState(app)

    def init_config(self, app):
        for k in dir(config):
            if k.startswith('OAREPO_OAI_'):
                app.config.setdefault(k, getattr(config, k))

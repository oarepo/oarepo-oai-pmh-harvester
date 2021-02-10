from typing import List, Dict, Any, Callable

from oarepo_oai_pmh_harvester.proxies import current_oai_client
from oarepo_oai_pmh_harvester.transformer import OAITransformer


def rule(provider, parser, path, phase=OAITransformer.PHASE_PRE):
    def wrapper(func):
        current_oai_client.add_rule(func, provider, parser, path, phase)

    return wrapper


def rule_error_handler(provider, parser):
    def wrapper(func):
        current_oai_client.add_error_handler(func, provider, parser)

    return wrapper


def parser(name):
    def wrapper(func):
        current_oai_client.add_parser(func, name)

    return wrapper


def endpoint_handler(provider: str = None, parser: str = None,
                     provider_parser_list: List[Dict] = None):
    if provider_parser_list and (provider or parser):
        raise Exception(
            "If the provider and parser is specified, cannot specify provider_parser_list")
    if (provider and not parser) or (parser and not provider):
        raise Exception("Must specify provider and parser")

    def wrapper(func):
        current_oai_client.add_endpoint_handler(func, provider=provider, parser_name=parser,
                                                provider_parser_list=provider_parser_list)

    return wrapper


def pre_processor(provider: str = None, parser: str = None,
                  provider_parser_list: List[Dict] = None) -> Callable:
    """
    Decorator that register function for pre processing. You can insert provider and parser or
    list of dict that contain more providers. Dict must have two keys provider and parser.


    :param provider: Name of provider, that is registred in config
    :type provider: str
    :param parser: Name of parser, that is registred in config
    :type parser: str
    :param provider_parser_list:
    :type provider_parser_list: List of dict with two keys (provider and parser)
    """
    if provider_parser_list and (provider or parser):
        raise Exception(
            "If the provider and parser is specified, cannot specify provider_parser_list")
    if (provider and not parser) or (parser and not provider):
        raise Exception("Must specify provider and parser")

    def wrapper(func):
        current_oai_client.add_pre_processor(func, provider=provider, parser_name=parser,
                                             provider_parser_list=provider_parser_list)

    return wrapper


def post_processor(provider: str = None, parser: str = None,
                   provider_parser_list: List[Dict] = None) -> Callable:
    """
    Decorator that register function for post processing. You can insert provider and parser or
    list of dict that contain more providers. Dict must have two keys provider and parser.


    :param provider: Name of provider, that is registred in config
    :type provider: str
    :param parser: Name of parser, that is registred in config
    :type parser: str
    :param provider_parser_list:
    :type provider_parser_list: List of dict with two keys (provider and parser)
    """
    if provider_parser_list and (provider or parser):
        raise Exception(
            "If the provider and parser is specified, cannot specify provider_parser_list")
    if (provider and not parser) or (parser and not provider):
        raise Exception("Must specify provider and parser")

    def wrapper(func):
        current_oai_client.add_post_processor(func, provider=provider, parser_name=parser,
                                              provider_parser_list=provider_parser_list)

    return wrapper

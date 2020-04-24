import logging
import sys

import click
from flask import cli
from invenio_db import db
from prettytable import PrettyTable
from sickle import Sickle
from sqlalchemy.orm.exc import NoResultFound

from invenio_oarepo_oai_pmh_harvester.exceptions import EndPointNotFoundError, \
    PrefixNotFoundError
from invenio_oarepo_oai_pmh_harvester.models import OAIProvider
from invenio_oarepo_oai_pmh_harvester.synchronization import OAISynchronizer

############################################################################
#                                   CLI                                    #
############################################################################

logging.basicConfig(level=logging.DEBUG)


@click.group()
def oai():
    """OAI harvester commands"""


@oai.command('synchronize')
@click.argument('provider', type=str)
@cli.with_appcontext
def synchronize(provider: str):
    try:
        provider_instance = OAIProvider.query.filter_by(code=provider).one()
    except NoResultFound:
        print(f"Provider \"{provider}\" is not defined in the database")
        sys.exit(1)
    sync = OAISynchronizer(provider_instance)
    sync.run()


# @oai.group()
# def stat():
#     pass


# @stat.command('fetch')
# @click.argument('provider', type=str)
# @cli.with_appcontext
# def get_stats(provider: str):
#     try:
#         provider_instance = OAIProvider.query.filter_by(code=provider).one()
#     except NoResultFound:
#         print(f"Provider \"{provider}\" is not defined in the database")
#         sys.exit(1)
#     stat_ = OAIStatsRunner(provider_instance)
#     stat_.run()


# @stat.command('process')
# @click.argument('data_set_id', type=int)
# @click.argument('provider', type=str)
# @cli.with_appcontext
# def process_data(data_set_id: int, provider: str):
#     # stat_instance = OAIStats.query.get(data_set_id)
#     # if stat_instance is None:
#     #     raise NoResultFound("The dataset is not exist")
#     try:
#         provider_instance = OAIProvider.query.filter_by(code=provider).one()
#     except NoResultFound:
#         print(f"Provider \"{provider}\" is not defined in the database")
#         sys.exit(1)
#     stat_processor = OAIStatsProcessor(provider_instance)
#     stat_processor.cwd = os.getcwd()
#     stat_processor.process_data()


# @stat.command('json')
# @click.argument('path')
# @cli.with_appcontext
# def upload_json(path: str):
#     if not os.path.exists(path):
#         raise FileNotFoundError
#     with open(path) as fp:
#         data = json.load(fp)
#     jsons = json.dumps(data, ensure_ascii=False)
#     stat_inst = OAIStats(provider_id=1, status="ok", result_json=jsons)
#     db.session.add(stat_inst)
#     db.session.commit()


@oai.group()
def register():
    pass


@register.command('provider')
@click.argument('provider_code', type=str)
@click.option('-d', '--description', type=str)
@click.option('-e', '--endpoint', type=str)
@click.option('-p', '--prefix', type=str, help="Metadata prefix (e.g.: xoai, marc, oai_dc)")
@click.option('-i', '--parser_id', type=int)
@cli.with_appcontext
def register_provider(provider_code: str, description: str, endpoint: str, prefix: str,
                      parser_id: int):
    """

    :param provider_code:
    :type provider_code:
    :param description:
    :type description:
    :param endpoint:
    :type endpoint:
    :param prefix:
    :type prefix:
    :param parser_id:
    :type parser_id:
    :return:
    :rtype:
    """
    provider = OAIProvider.query.filter_by(code=provider_code).one_or_none()
    if provider is None:
        if endpoint is None:
            raise EndPointNotFoundError(
                "When you create new provider you have to insert its end_point")
        sickle = Sickle(endpoint)
        res_formats = sickle.ListMetadataFormats()
        md_formats = []
        for format_ in res_formats:
            md_formats.append(format_.metadataPrefix)
        if prefix is None:
            raise PrefixNotFoundError(
                "When you create new provider you have to insert its metadata format prefix. \n "
                "Available formats for the provider are:\n {}".format('\n'.join(md_formats)))

        provider = OAIProvider(code=provider_code, oai_endpoint=endpoint,
                               metadata_prefix=prefix)
        db.session.add(provider)
    if description:
        provider.description = description
    if endpoint:
        provider.oai_endpoint = endpoint
    if prefix:
        provider.metadata_prefix = prefix
    if parser_id:
        provider.oai_parser_id = parser_id
    db.session.commit()


# @register.command('parsers')
# @cli.with_appcontext
# def parsers():
#     parser_registry.load()
#     parsers_ = parser_registry.parsers
#     for k, v in parsers_.items():
#         code = k.strip()
#         description = v.__doc__.strip()
#         existed_parser = OAIParser.query.filter_by(code=code).one_or_none()
#         if existed_parser is None:
#             rule = OAIParser(code=code, description=description)
#             print("Rule", rule, db.engine)
#             db.session.add(rule)
#             db.session.commit()


# @register.command('rules')
# @cli.with_appcontext
# def rules():
#     rule_registry.load()
#     rules_ = rule_registry.rules
#     for k, v in rules_.items():
#         code = k.strip()
#         description = v.__doc__
#         if description is not None:
#             description = description.strip()
#         existed_rule = OAIRule.query.filter_by(code=code).one_or_none()
#         if existed_rule is None:
#             rule = OAIRule(code=code, description=description)
#             db.session.add(rule)
#             db.session.commit()


# @register.command('stats')
# @cli.with_appcontext
# def stats():
#     rule_registry.load()
#     stats_ = rule_registry.stats
#     for k, v in stats_.items():
#         code = k.strip()
#         description = v.__doc__
#         if description is not None:
#             description = description.strip()
#         existed_rule = OAIStatRules.query.filter_by(code=code).one_or_none()
#         if existed_rule is None:
#             rule = OAIStatRules(code=code, description=description)
#             db.session.add(rule)
#             db.session.commit()


@oai.group("provider")
def provider_group():
    pass


@provider_group.command('list')
@cli.with_appcontext
def list_provider():
    """

    :return:
    :rtype:
    """
    providers = OAIProvider.query.all()
    tb = PrettyTable()
    tb.field_names = ["id", "code", "description", "oai_endpoint", "metadata_prefix",
                      "oai_parser_id"]
    for provider_ in providers:
        tb.add_row([provider_.id, provider_.code, provider_.description, provider_.oai_endpoint,
                    provider_.metadata_prefix, provider_.oai_parser_id])

    print(tb)


# @provider_group.command('rule')
# @click.argument("code")
# @click.option("-i", "--rule_id", default=None, type=int)
# @click.option("-c", "--rule_code", default=None)
# @cli.with_appcontext
# def add_rule(code: str, rule_id: int, rule_code: str) -> None:
#     """
#     Assign rule to provider.
#     :param code: Provider code
#     :type code: str
#     :param rule_id:
#     :type rule_id: int
#     :param rule_code:
#     :type rule_code: str
#     :return: None
#     :rtype: None
#     """
#     provider = OAIProvider.query.filter_by(code=code).one_or_none()
#     if provider is None:
#         raise ProviderNotFoundError("Required provider has not been found. Please try again.")
#     if rule_id:
#         rule = OAIRule.query.get(rule_id)
#         provider.rules.append(rule)
#         db.session.commit()
#         return
#     if rule_code:
#         rule = OAIRule.query.filter_by(code=rule_code).one()
#         provider.rules.apped(rule)
#         db.session.commit()
#     raise RuleRequiredError("rule_id or rule_code is required")


# @provider_group.command('stat')
# @click.argument("code")
# @click.option("-i", "--stat_id", default=None, type=int)
# @click.option("-c", "--stat_code", default=None)
# @cli.with_appcontext
# def add_stat(code: str, stat_id: int, stat_code: str) -> None:
#     """
#     Assign stat script to the provider.
#     :param code: Provider code
#     :type code: str
#     :param stat_id:
#     :type stat_id: int
#     :param stat_code:
#     :type stat_code: str
#     :return: None
#     :rtype: None
#     """
#     provider = OAIProvider.query.filter_by(code=code).one_or_none()
#     if provider is None:
#         raise ProviderNotFoundError("Required provider has not been found. Please try again.")
#     if stat_id:
#         stat = OAIStatRules.query.get(stat_id)
#         provider.stats.append(stat)
#         db.session.commit()
#         return
#     if stat_code:
#         stat = OAIStatRules.query.filter_by(code=stat_code).one()
#         provider.stats.apped(stat)
#         db.session.commit()
#     raise RuleRequiredError("stat_id or stat_code is required")


@oai.group('rules')
def rules_group():
    pass


# @rules_group.command('list')
# @cli.with_appcontext
# def list_rules():
#     """
#
#     :return:
#     :rtype:
#     """
#     rules_ = OAIRule.query.all()
#     tb = PrettyTable()
#     tb.field_names = ["id", "code", "description"]
#     for rule in rules_:
#         tb.add_row([rule.id, rule.code, rule.description])
#     print(tb)


@oai.group('parsers')
def parsers_group():
    pass

# @parsers_group.command('list')
# @cli.with_appcontext
# def list_parsers():
#     """
#
#     :return:
#     :rtype:
#     """
#     parsers_ = OAIParser.query.all()
#     tb = PrettyTable()
#     tb.field_names = ["id", "code", "description"]
#     for parser in parsers_:
#         tb.add_row([parser.id, parser.code, parser.description])
#     print(tb)

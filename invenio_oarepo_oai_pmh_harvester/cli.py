import logging
import sys

import click
from flask import cli
from invenio_records.models import RecordMetadata
from sickle import Sickle
from sqlalchemy.orm.exc import NoResultFound

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

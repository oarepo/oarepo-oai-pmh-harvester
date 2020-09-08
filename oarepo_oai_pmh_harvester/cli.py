import json

import click
from click import STRING, File
from flask import cli
from invenio_db import db

from oarepo_oai_pmh_harvester.models import OAIProvider


@click.group()
def oai():
    """OAI harvester commands"""


@oai.group()
def register():
    pass


@register.command("provider")
@click.option('-c', '--code', required=True, help="The unique code that define provider",
              type=STRING)
@click.option('-d', '--description', help="Provider description")
@click.option('-e', '--end_point', 'ep', required=True, help="Provider endpoint - url address")
@click.option('-s', '--set', 'set_', help="Name of OAI set")
@click.option('-p', '--prefix', help="Metadata prefix")
@click.option('-f', '--file', 'constant_fields', type=File(),
              help="Path to the json file where is stored constant fields")
@cli.with_appcontext
def register_provider(code, ep, description=None, set_=None, prefix=None, constant_fields=None):
    provider = OAIProvider.query.filter_by(code=code).one_or_none()
    if provider:
        click.secho(f"Provider with code '{code}' already exists. For update call update method ("
                    f"invenio oai update provider [options])", bg='yellow', fg='red')
        return
    if constant_fields:
        constant_fields = json.load(constant_fields)
    provider = OAIProvider(code=code, description=description, oai_endpoint=ep, set_=set_,
                           metadata_prefix=prefix, constant_fields=constant_fields)
    db.session.add(provider)
    db.session.commit()

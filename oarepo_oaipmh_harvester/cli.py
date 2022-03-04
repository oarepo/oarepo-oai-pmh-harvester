import click

from oarepo_oaipmh_harvester.models import OAIHarvesterConfig
from oarepo_oaipmh_harvester.proxies import current_harvester
from flask.cli import with_appcontext

from invenio_db import db


@click.group(name='oaiharvester')
def oaiharvester():
    """Classifier commands."""


@oaiharvester.command()
@click.option('-a', '--all-records', default=False, is_flag=True,
              help="Re-harvest all records, not from the last timestamp")
@click.option('--background', default=False, is_flag=True,
              help="Harvest on background via celery task")
@click.option('--dump-to',
              help="Do not import records, just dump (cache) them to this directory (mostly for debugging)")
@click.option('--load-from',
              help="Do not contact oai-pmh server but load the records from this directory (created by dump-to option)")
@click.argument('harvester_code')
@click.argument('identifiers', nargs=-1)
@with_appcontext
def harvest(harvester_code, all_records, background, dump_to, load_from, identifiers):
    current_harvester.run(harvester_code, all_records=all_records, on_background=background,
                          load_from=load_from, dump_to=dump_to, identifiers=identifiers)


@oaiharvester.command()
@click.option('--code', help="OAI server code", required=True)
@click.option('--name', help="OAI server name", required=True)
@click.option('--url', help="OAI base url", required=True)
@click.option('--set', help="OAI set", required=True)
@click.option('--prefix', help="OAI metadata prefix", required=True)
@click.option('--parser', help="OAI metadata parser", required=False)
@click.option('--transformer', help="Transformer class", required=True)
@with_appcontext
def add(code, name, url, set, prefix, parser, transformer):
    harvester = OAIHarvesterConfig.query.filter_by(code=code).one_or_none()
    if harvester:
        print(f"Harvester with code {code} already exists")
        return
    db.session.add(OAIHarvesterConfig(
        code=code,
        name=name,
        baseurl=url,
        metadataprefix=prefix,
        setspecs=set,
        parser=parser,
        transformer=transformer
    ))
    db.session.commit()

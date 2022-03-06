from collections import defaultdict

import click

from oarepo_oaipmh_harvester.models import OAIHarvesterConfig, OAIHarvestRun, OAIHarvestRunBatch, HarvestStatus
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


@oaiharvester.command()
@click.argument('code', required=True)
@click.option('--run-id', required=False)
@click.option('--details', default=False, is_flag=True)
@with_appcontext
def warnings(code, run_id=None, details=False):
    cfg = OAIHarvesterConfig.query.filter_by(code=code).one()
    if run_id is not None:
        run_query = OAIHarvestRun.query.filter_by(id=run_id, harvester_id=cfg.id)
    else:
        run_query = OAIHarvestRun.query.filter_by(harvester_id=cfg.id).order_by(OAIHarvestRun.started.desc())
    run = run_query.first()
    if not run:
        print("No run to display")
        return
    batches = OAIHarvestRunBatch.query.filter_by(run_id=run.id).filter(OAIHarvestRunBatch.status.in_([
        HarvestStatus.WARNING, HarvestStatus.FAILED
    ]))
    by_message = defaultdict(list)
    for batch in batches:
        if batch.warning_records:
            for k, vv in batch.warning_records.items():
                for v in vv:
                    if details:
                        by_message[v['message']].append(k)
                    else:
                        by_message[v['message'][:80]].append(k)
    for msg, records in sorted(list(by_message.items()), key=lambda x: -len(x[1])):
        if details:
            print(f'{msg:80s} || {", ".join(records)}')
        else:
            print(f'{msg:80s} || {len(records):10d} || {", ".join(records[:3])}')


@oaiharvester.command()
@click.argument('code', required=True)
@click.option('--run-id', required=False)
@click.option('--details', default=False, is_flag=True)
@with_appcontext
def errors(code, run_id=None, details=False):
    cfg = OAIHarvesterConfig.query.filter_by(code=code).one()
    if run_id is not None:
        run_query = OAIHarvestRun.query.filter_by(id=run_id, harvester_id=cfg.id)
    else:
        run_query = OAIHarvestRun.query.filter_by(harvester_id=cfg.id).order_by(OAIHarvestRun.started.desc())
    run = run_query.first()
    if not run:
        print("No run to display")
        return
    batches = OAIHarvestRunBatch.query.filter_by(run_id=run.id, status=HarvestStatus.FAILED)
    by_message = defaultdict(list)
    for batch in batches:
        if batch.failed_records:
            for k, vv in batch.failed_records.items():
                for v in vv:
                    if details:
                        by_message[v['message']].append(k)
                    else:
                        by_message[v['message'][:80].replace('\n', ' ')].append(k)
    for msg, records in sorted(list(by_message.items()), key=lambda x: -len(x[1])):
        if details:
            print(f'{msg:80s} || {", ".join(records)}')
        else:
            print(f'{msg:80s} || {len(records):10d} || {", ".join(records[:3])}')

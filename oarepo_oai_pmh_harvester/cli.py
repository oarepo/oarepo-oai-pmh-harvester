import json
from collections import defaultdict
from pprint import pprint

import click
from boltons.tbutils import ParsedException
from flask import cli

from oarepo_oai_pmh_harvester.models import OAIRecordExc, OAISync
from oarepo_oai_pmh_harvester.proxies import current_oai_client


@click.group()
def oai():
    """
    Oai harvester commands
    """
    pass


@oai.command("run")
@click.option("-p", "--provider", "provider", multiple=True, default=None,
              help="Code name of provider, defined in invenio.cfg")
@click.option("-s", "--synchronizer", "synchronizer", multiple=True, default=None,
              help="Code name of OAI-PMH setup, defined in invenio.cfg")
@click.option('--break/--no-break', 'break_on_error',
              help="Break on error, if true program is terminated when record cause error",
              default=True
              )
@click.option('-o', '--start_oai', default=None,
              help="OAI identifier from where synchronization begin")
@click.option("-i", "--start_id", default=0, type=int,
              help="The serial number from which the synchronization starts. This is useful if "
                   "for some reason the previous synchronization was interrupted at some point.")
@click.option("-a", "--oai", default=None, type=str, multiple=True,
              help="OAI identifier that will be fetched and synchronized. The field is "
                   "repeatable. If this option is used, the provider and synchronizer must be "
                   "specified and "
                   "star_id or start_oai must not be used")
@click.option('--overwrite/--no-overwrite', 'overwrite',
              help="Overwriter record with the same timestamp. Default option is false",
              default=False
              )
@click.option('--bulk/--no-bulk', 'bulk',
              help="Specifies whether a bulk request (ListRecords) is called or a request is "
                   "called individually (GetRecord). Bulk processing is suitable for "
                   "synchronizing the entire set, and contrary for individual records."
                   "Option is working only for -a/--oai option, otherwise bulk is set in config "
                   "file",
              default=True
              )
@cli.with_appcontext
def run(provider, synchronizer, break_on_error, start_oai, start_id, oai, overwrite, bulk):
    """
    Starts harvesting the resources set in invenio.cfg through the OAREPO_OAI_PROVIDERS
    environment variable.
    """
    l = len(oai)
    if l > 0 and provider and synchronizer and not start_oai and not start_id:
        assert len(provider) <= 1, "OAI option is only for one provider and synchronizer"
        assert len(synchronizer) <= 1, "OAI option is only for one provider and synchronizer"
        provider = provider[0]
        synchronizer = synchronizer[0]
        current_oai_client.run_synchronizer_by_ids(
            list(oai),
            provider,
            synchronizer,
            break_on_error=break_on_error,
            overwrite=overwrite,
            bulk=bulk
        )
    else:
        assert l == 0, " If OAI option is used, the provider and synchronizer must be " \
                       "specified and star_id or start_oai must not be used"
        if not provider:
            provider = None
        else:
            provider = list(provider)
        if not synchronizer:
            synchronizer = None
        else:
            synchronizer = list(synchronizer)
        current_oai_client.run(providers_codes=provider, synchronizers_codes=synchronizer,
                               break_on_error=break_on_error, start_oai=start_oai,
                               start_id=start_id)


@oai.command("fix")
@click.option("-p", "--provider", "provider", default=None,
              help="Code name of provider, defined in invenio.cfg")
@click.option("-s", "--synchronizer", "synchronizer", default=None,
              help="Code name of OAI-PMH setup, defined in invenio.cfg")
@click.option("-i", "--sync-id", "sync_id", default=None,
              help="Database id of synchonization", type=int)
@click.option('--break/--no-break', 'break_on_error',
              help="Break on error, if true program is terminated when record cause error",
              default=True
              )
@cli.with_appcontext
def fix_erroneous(provider, synchronizer, sync_id, break_on_error):
    """
    Run synchronization of erroneous records.
    """
    if sync_id:
        if provider or synchronizer:
            print("Provider and synchronizer is ignored, because sync_id was provided.")
        sync = OAISync.query.get(sync_id)
        provider = sync.provider_code
        synchronizer = sync.synchronizer_code
    elif provider and synchronizer:
        sync_id_array = OAISync.query.filter_by(provider_code=provider,
                                                synchronizer_code=synchronizer).all()
        if sync_id_array:
            sync_id = sync_id_array[-1].id
        else:
            raise Exception(
                f"There is no synchronization for {provider} and {synchronizer} synchronizer code")
    else:
        raise Exception("Sync_id or provider code with synchronizer code must be specified")
    records = OAIRecordExc.query.filter_by(oai_sync_id=sync_id).all()
    ids = [record.oai_identifier for record in records]
    current_oai_client.run_synchronizer_by_ids(list(ids), provider, synchronizer,
                                               break_on_error=break_on_error,
                                               overwrite=True)


@oai.command("group_errors")
@click.option("-i", "--sync-id", "id_", help="Synchronization id")
@click.option("-o", "--output", "output", help="Synchronization id")
@cli.with_appcontext
def group_errors(id_, output=None):
    """
    Return dict with errors grouped by type of error
    """
    errors = OAIRecordExc.query.filter_by(oai_sync_id=id_).all()
    result = defaultdict(list)
    for error in errors:
        print(error.oai_identifier)
        tb = error.traceback
        tb_formated = ParsedException.from_string(tb)
        key = tb_formated.exc_msg
        assert isinstance(key, str)
        result[key].append(error.oai_identifier)
    result = dict(result)
    if output:
        f = open(output+'/errors.json', 'w+')
        json.dump(result, f, ensure_ascii=False)
    else:
        print(result.keys())


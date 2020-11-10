import click
from flask import cli

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
@cli.with_appcontext
def run(provider, synchronizer, break_on_error, start_oai, start_id):
    """
    Starts harvesting the resources set in invenio.cfg through the OAREPO_OAI_PROVIDERS
    environment variable.
    """
    if not provider:
        provider = None
    else:
        provider = list(provider)
    if not synchronizer:
        synchronizer = None
    else:
        synchronizer = list(synchronizer)
    current_oai_client.run(providers_codes=provider, synchronizers_codes=synchronizer,
                           break_on_error=break_on_error, start_oai=start_oai, start_id=start_id)

# TODO: použít minter/nepoužít minter

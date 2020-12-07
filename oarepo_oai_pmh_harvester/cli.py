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
@click.option("-a", "--oai", default=None, type=str, multiple=True,
              help="OAI identifier that will be fetched and synchronized. The field is "
                   "repeatable. If this option is used, the provider and synchronizer must be "
                   "specified and "
                   "star_id or start_oai must not be used")
@cli.with_appcontext
def run(provider, synchronizer, break_on_error, start_oai, start_id, oai):
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
        current_oai_client.run_synchronizer_by_ids(list(oai), provider, synchronizer,
                                                   break_on_error=break_on_error)
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

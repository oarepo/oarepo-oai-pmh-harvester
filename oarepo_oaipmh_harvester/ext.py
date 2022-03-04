import datetime
from functools import cached_property
from typing import Union

import pkg_resources

from .cli import oaiharvester as oaiharvester_cmd
from .harvester import oai_harvest
from .models import OAIHarvesterConfig


class OARepoOAIHarvesterExt(object):
    """extension."""

    def __init__(self, app=None):
        """Extension initialization."""
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Flask application initialization."""
        app.cli.add_command(oaiharvester_cmd)
        app.extensions["oarepo_oaipmh_harvester"] = self

    def run(self, harvester_or_code: Union[str, OAIHarvesterConfig], all_records=False,
            on_background=False, dump_to=None, load_from=None, identifiers=None):
        harvester: OAIHarvesterConfig
        if isinstance(harvester_or_code, str):
            try:
                harvester = OAIHarvesterConfig.query.filter_by(code=harvester_or_code).one()
            except:
                raise ValueError(f'No OAIHarvester was found for code "{harvester_or_code}"')
        else:
            harvester = harvester_or_code

        start_date = '1970-01-01'

        if not all_records and not identifiers:
            start_date = harvester.get_last_record_date() or start_date

        if on_background:
            oai_harvest.delay(harvester.id, start_date,
                              load_from=load_from, dump_to=dump_to, on_background=on_background,
                              identifiers=identifiers)
        else:
            oai_harvest.apply(
                args=(harvester.id, start_date),
                kwargs=dict(load_from=load_from, dump_to=dump_to, on_background=on_background,
                            identifiers=identifiers))

    @cached_property
    def oai_parsers(self):
        ret = {}
        for ep in pkg_resources.iter_entry_points('oarepo_oaipmh_harvester.parsers'):
            ret[ep.name] = ep.load()
        return ret

    def get_parser(self, prefix):
        try:
            return self.oai_parsers[prefix]
        except KeyError:
            raise KeyError(f'OAI parser for prefix {prefix} has not been registered. '
                           f'Is it in entry points?')

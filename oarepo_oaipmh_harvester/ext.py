import datetime
from functools import cached_property
from typing import Union

import pkg_resources

from .cli import oaiharvester as oaiharvester_cmd
from .harvester import oai_harvest
from .models import OAIHarvesterConfig
from .oaipmh_config.records.api import OaipmhConfigRecord
from .oaipmh_config.records.models import OaipmhConfigMetadata
from oarepo_oaipmh_harvester.oaipmh_config.proxies import current_service as config_service
from oarepo_oaipmh_harvester.oaipmh_run.proxies import current_service as run_service
from invenio_access.permissions import system_identity
from invenio_pidstore.resolver import Resolver


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

    def run(self, harvester_or_code: Union[str, OaipmhConfigRecord], all_records=False,
            on_background=False, dump_to=None, load_from=None, identifiers=None):

        # harvester:  OaipmhConfigRecord
        harvester = None
        if isinstance(harvester_or_code, str):
            harvesters = config_service.scan(system_identity, params={'facets': {'metadata_code': [harvester_or_code]}})
            # harvesters = OaipmhConfigMetadata.query.all()

            # for h in harvesters:
            #     if h.json['metadata']['code'] == harvester_or_code:
            #         harvester_id = h.json['id']
            #         break

            try:

                # print(list(harvesters.hits)[0]['id'])
                # print('jej')
                hits = list(harvesters.hits)
                harvester_id = hits[0]['id']
                print(harvester_id)
                harvester = config_service.read(system_identity, harvester_id).data
                # harvester = OaipmhConfigMetadata.query.filter_by(code=harvester_or_code).one()
            except Exception as e:
                print(e)
                # raise ValueError(f'No OAIHarvester was found for code "{harvester_or_code}"')
        else:
            harvester = harvester_or_code

        start_date = '1970-01-01'
        if not all_records and not identifiers:
            harvest_runs = []
            for hit in (run_service.read_all(system_identity, ['metadata']).to_dict())['hits']['hits']:
                if hit['metadata']['harvester_id'] == harvester['id'] and 'last_datestamp' in hit['metadata']:
                    harvest_runs.append(hit['metadata']['last_datestamp'])

            harvest_runs = list(filter(('null').__ne__, harvest_runs))

            sorted_runs = sorted(harvest_runs)
            if len(sorted_runs) == 0:
                start_date_from_run = None
            else:
                start_date_from_run = sorted_runs[-1]

            start_date = start_date_from_run or start_date
            if start_date == 'null':
                start_date = None
        if on_background:
            oai_harvest.delay(harvester['id'], start_date,
                              load_from=load_from, dump_to=dump_to, on_background=on_background,
                              identifiers=identifiers)
        else:
            oai_harvest.apply(
                args=(harvester['id'], start_date),
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

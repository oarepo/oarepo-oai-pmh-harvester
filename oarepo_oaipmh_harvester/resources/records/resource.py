from flask_resources import resource_requestctx, response_handler, route
from flask_resources.resources import Resource
from invenio_records_resources.resources.errors import ErrorHandlersMixin
from invenio_records_resources.resources.records.resource import request_view_args
from oarepo_oaipmh_harvester.oai_harvester.proxies import (
            current_service as harvester_service,
        )
from invenio_access.permissions import system_identity
from oarepo_oaipmh_harvester.tasks import harvest_task


class HarvestResource(Resource, ErrorHandlersMixin):
    def __init__(self, config, service):
        super().__init__(config)
        self.service = service

    def create_url_rules(self):
        """Create the URL rules for the record resource."""
        routes = self.config.routes
        url_rules = [
            route("GET", routes["execute"], self.execute),
        ]
        return url_rules

    @request_view_args
    @response_handler(many=True)
    def execute(self, *args, **kwargs):

        harvesters = list(
            harvester_service.scan(
                system_identity,
                params={"facets": {"id": [resource_requestctx.view_args["harvester_code"]]}},
            )
        )

        harvest_task.delay(harvesters[0])

        return "Harvesting started on the background", 200

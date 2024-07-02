from flask import g
from flask_resources import resource_requestctx, response_handler, route
from flask_resources.resources import Resource
from invenio_records_resources.resources.errors import ErrorHandlersMixin
from invenio_records_resources.resources.records.resource import request_search_args
from invenio_records_resources.resources.records.resource import (
    request_data,
    request_extra_args,
    request_headers,
    request_view_args,
)

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
    @request_data
    @request_extra_args
    @request_search_args
    @request_headers
    @response_handler(many=True)
    def execute(self, *args, **kwargs):

        harvest_task.delay(code = resource_requestctx.view_args["harvester_code"])


        return "", 200

"""OAI Run resource config."""

import marshmallow as ma
from flask import g
from flask_resources import resource_requestctx, response_handler, route
from invenio_records_resources.resources import (
    RecordResource,
    RecordResourceConfig,
)
from invenio_records_resources.resources.errors import ErrorHandlersMixin
from invenio_records_resources.resources.records.resource import (
    request_search_args,
    request_view_args,
)
from invenio_records_resources.resources.records.utils import search_preference

from oarepo_oaipmh_harvester.administration.record.api import response_handlers


#
# Resource config
#
class OAIRecordResourceConfig(RecordResourceConfig):
    """OAI Runs resource configuration."""

    blueprint_name = "oai_records"
    url_prefix = "/oai/harvest/records"
    routes = {
        "list": "",
        "item": "/<path:id>",
        "harvest": "/<path:id>/harvest",
    }

    request_view_args = {
        "id": ma.fields.Str(),
    }

    error_handlers = {
        **ErrorHandlersMixin.error_handlers,
    }

    response_handlers = {
        **response_handlers,
        "application/vnd.inveniordm.v1+json": RecordResourceConfig.response_handlers[
            "application/json"
        ],
        **RecordResourceConfig.response_handlers,
    }


class OAIRecordResource(RecordResource):

    def p(self, prefix, route):
        """Prefix a route with the URL prefix."""
        return f"{prefix}{route}"

    def create_url_rules(self):
        """Create the URL rules for the users resource."""
        routes = self.config.routes
        return [
            route("GET", routes["list"], self.search),
            route("GET", routes["item"], self.read),
            route("POST", routes["harvest"], self.harvest),
        ]

    @request_search_args
    @request_view_args
    @response_handler(many=True)
    def search(self):
        """Perform a search over users."""
        hits = self.service.search(
            identity=g.identity,
            params=resource_requestctx.args,
            search_preference=search_preference(),
        )
        return hits.to_dict(), 200

    @request_view_args
    @response_handler()
    def read(self):
        """Read a user."""
        item = self.service.read(
            id_=resource_requestctx.view_args["id"],
            identity=g.identity,
        )
        return item.to_dict(), 200

    @request_view_args
    @response_handler()
    def harvest(self):
        """Re-harvest the OAI record."""
        item = self.service.harvest(
            id_=resource_requestctx.view_args["id"],
            identity=g.identity,
        )
        return item.to_dict(), 200

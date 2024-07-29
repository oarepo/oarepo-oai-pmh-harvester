from flask_resources import resource_requestctx, response_handler, route
from invenio_administration.permissions import administration_permission
from invenio_records_resources.resources import RecordResource
from invenio_records_resources.proxies import current_service_registry
from invenio_records_resources.resources.records.resource import request_view_args

from oarepo_oaipmh_harvester.tasks import harvest_task


class OaiHarvesterBaseResource(RecordResource):
    """OaiHarvesterRecord resource."""

    def create_url_rules(self):
        """Create the URL rules for the record resource."""
        routes = self.config.routes
        url_rules = super().create_url_rules()
        url_rules.append(route("GET", routes["harvest"], self.harvest))
        return url_rules

    @property
    def api_service(self):
        return current_service_registry.get(self.config.api_service)

    @request_view_args
    @administration_permission.require(http_exception=403)
    @response_handler(many=True)
    def harvest(self, *args, **kwargs):
        harvester = self.api_service.read(
            g.identity, resource_requestctx.view_args["pid_value"]
        )
        harvest_task.delay(harvester.to_dict())

        return "Harvesting started on the background.", 200

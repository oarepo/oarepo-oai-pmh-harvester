import importlib_metadata
from flask_resources import ResponseHandler

from oarepo_oaipmh_harvester.common.resources.records.harvester_config import (
    OaiHarvesterBaseResourceConfig,
)
from oarepo_oaipmh_harvester.oai_harvester.resources.records.ui import (
    OaiHarvesterUIJSONSerializer,
)


class OaiHarvesterResourceConfig(OaiHarvesterBaseResourceConfig):
    """OaiHarvesterRecord resource config."""

    blueprint_name = "oarepo-oaipmh-harvester"
    url_prefix = "/oai/harvest/harvesters/"

    @property
    def response_handlers(self):
        entrypoint_response_handlers = {}
        for x in importlib_metadata.entry_points(
            group="invenio.oarepo_oaipmh_harvester.oai_harvester.response_handlers"
        ):
            entrypoint_response_handlers.update(x.load())
        return {
            "application/vnd.inveniordm.v1+json": ResponseHandler(
                OaiHarvesterUIJSONSerializer()
            ),
            **super().response_handlers,
            **entrypoint_response_handlers,
        }

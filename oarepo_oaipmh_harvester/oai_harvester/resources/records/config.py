import importlib_metadata
from flask_resources import ResponseHandler
from invenio_records_resources.resources import RecordResourceConfig

from oarepo_oaipmh_harvester.oai_harvester.resources.records.ui import (
    OaiHarvesterUIJSONSerializer,
)


class OaiHarvesterResourceConfig(RecordResourceConfig):
    """OaiHarvesterRecord resource config."""

    blueprint_name = "OaiHarvester"
    url_prefix = "/oarepo-oaipmh-harvester.oai-harvester/"

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

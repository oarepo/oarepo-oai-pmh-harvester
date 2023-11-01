import importlib_metadata
from flask_resources import ResponseHandler
from invenio_records_resources.resources import RecordResourceConfig

from oarepo_oaipmh_harvester.oai_run.resources.records.ui import OaiRunUIJSONSerializer


class OaiRunResourceConfig(RecordResourceConfig):
    """OaiRunRecord resource config."""

    blueprint_name = "oarepo-oaipmh-run"
    url_prefix = "/oai/harvest/runs/"

    @property
    def response_handlers(self):
        entrypoint_response_handlers = {}
        for x in importlib_metadata.entry_points(
            group="invenio.oarepo_oaipmh_harvester.oai_run.response_handlers"
        ):
            entrypoint_response_handlers.update(x.load())
        return {
            "application/vnd.inveniordm.v1+json": ResponseHandler(
                OaiRunUIJSONSerializer()
            ),
            **super().response_handlers,
            **entrypoint_response_handlers,
        }

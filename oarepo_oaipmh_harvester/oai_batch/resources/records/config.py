import importlib_metadata
from flask_resources import ResponseHandler
from invenio_records_resources.resources import RecordResourceConfig

from oarepo_oaipmh_harvester.oai_batch.resources.records.ui import (
    OaiBatchUIJSONSerializer,
)


class OaiBatchResourceConfig(RecordResourceConfig):
    """OaiBatchRecord resource config."""

    blueprint_name = "OaiBatch"
    url_prefix = "/oarepo-oaipmh-harvester.oai-batch/"

    @property
    def response_handlers(self):
        entrypoint_response_handlers = {}
        for x in importlib_metadata.entry_points(
            group="invenio.oarepo_oaipmh_harvester.oai_batch.response_handlers"
        ):
            entrypoint_response_handlers.update(x.load())
        return {
            "application/vnd.inveniordm.v1+json": ResponseHandler(
                OaiBatchUIJSONSerializer()
            ),
            **super().response_handlers,
            **entrypoint_response_handlers,
        }

import importlib_metadata
from flask_resources import ResponseHandler
from invenio_records_resources.resources import RecordResourceConfig

from oarepo_oaipmh_harvester.oai_record.resources.records.ui import (
    OaiRecordUIJSONSerializer,
)


class OaiRecordResourceConfig(RecordResourceConfig):
    """OaiRecordRecord resource config."""

    blueprint_name = "OaiRecord"
    url_prefix = "/oarepo-oaipmh-harvester.oai-record/"

    @property
    def response_handlers(self):
        entrypoint_response_handlers = {}
        for x in importlib_metadata.entry_points(
            group="invenio.oarepo_oaipmh_harvester.oai_record.response_handlers"
        ):
            entrypoint_response_handlers.update(x.load())
        return {
            "application/vnd.inveniordm.v1+json": ResponseHandler(
                OaiRecordUIJSONSerializer()
            ),
            **super().response_handlers,
            **entrypoint_response_handlers,
        }

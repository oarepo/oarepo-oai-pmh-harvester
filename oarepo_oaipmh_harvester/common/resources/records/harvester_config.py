import importlib_metadata
from flask_resources import ResponseHandler
from invenio_records_resources.resources import RecordResourceConfig

from oarepo_oaipmh_harvester.oai_harvester.resources.records.ui import (
    OaiHarvesterUIJSONSerializer,
)


class OaiHarvesterBaseResourceConfig(RecordResourceConfig):
    """OaiHarvesterRecord resource config."""

    api_service = "oarepo-oaipmh-harvesters"
    routes = {
        "list": "",
        "item": "/<pid_value>",
        "harvest": "/<pid_value>/harvest",
    }

from flask_resources import JSONSerializer, ResponseHandler
from invenio_records_resources.resources import (
    RecordResourceConfig as InvenioRecordResourceConfig,
)

from .serializers_to_be_moved.ui import UIJSONSerializer


class NrThesesMetadataResourceConfig(InvenioRecordResourceConfig):
    """NrThesesMetadataRecord resource config."""

    blueprint_name = "NrThesesMetadata"
    url_prefix = "/nr_theses_metadata/"

    response_handlers = {
        "application/json": ResponseHandler(JSONSerializer()),
        "application/vnd.inveniordm.v1+json": ResponseHandler(UIJSONSerializer()),
    }
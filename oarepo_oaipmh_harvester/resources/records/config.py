
from invenio_records_resources.resources.records.config import RecordResourceConfig
import marshmallow as ma


class HarvestResourceConfig(RecordResourceConfig):
    blueprint_name = "harvest"
    url_prefix = "/harvest"
    routes = {
        "execute": "/<harvester_code>/execute",
    }
    request_view_args = {"harvester_code": ma.fields.Str()}

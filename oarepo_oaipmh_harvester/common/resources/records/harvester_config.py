from invenio_records_resources.resources import RecordResourceConfig


class OaiHarvesterBaseResourceConfig(RecordResourceConfig):
    """OaiHarvesterRecord resource config."""

    api_service = "oarepo-oaipmh-harvesters"
    routes = {
        "list": "",
        "item": "/<pid_value>",
        "harvest": "/<pid_value>/start",
    }

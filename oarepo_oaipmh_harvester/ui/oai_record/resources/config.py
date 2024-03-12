from oarepo_ui.resources.config import RecordsUIResourceConfig


class OAIRecordUIResourceConfig(RecordsUIResourceConfig):
    template_folder = "../templates"
    url_prefix = "/oai/harvest/records/"
    blueprint_name = "oai-record-ui"
    ui_serializer_class = "oarepo_oaipmh_harvester.oai_record.resources.records.ui.OaiRecordUIJSONSerializer"
    api_service = "oarepo-oaipmh-records"
    layout = "oarepo-oaipmh-record"

    application_id = "oai_record_ui"

    templates = {
        "detail": "oai_record_ui.OaiRecordDetail",
        "search": "oai_record_ui.OaiRecordSearch",
    }
    routes = {
        "search": "",
        "detail": "/<pid_value>",
        "export": "/<pid_value>/export/<export_format>",
    }

    def search_active_facets(self, api_config, identity):
        return list(self.search_available_facets(api_config, identity).keys())

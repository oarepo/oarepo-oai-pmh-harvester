from oarepo_ui.resources.config import RecordsUIResourceConfig


class OAIRecordUIResourceConfig(RecordsUIResourceConfig):
    template_folder = "../templates"
    url_prefix = "/oai/harvest/records/"
    blueprint_name = "oai-record-ui"
    ui_serializer_class = "oarepo_oaipmh_harvester.oai_record.resources.records.ui.OaiRecordUIJSONSerializer"
    api_service = "oarepo-oaipmh-records"
    layout = "oarepo-oaipmh-record"

    templates = {
        "detail": {
            "layout": "oai_record_ui/OaiRecordDetail.jinja",
            "blocks": {
                "record_main_content": "OaiRecordMain",
                "record_sidebar": "OaiRecordSidebar",
            },
        },
        "search": {
            "layout": "oai_record_ui/OaiRecordSearch.jinja",
            "app_id": "OaiRecord.Search",
        },
    }

    routes = {
        "search": "",
        "detail": "/<pid_value>",
        "export": "/<pid_value>/export/<export_format>",
    }

    def search_active_facets(self, api_config, identity):
        return list(self.search_available_facets(api_config, identity).keys())

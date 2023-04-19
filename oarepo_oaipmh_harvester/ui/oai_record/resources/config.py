from oarepo_ui.resources.config import RecordsUIResourceConfig
import marshmallow as ma


class OAIRecordUIResourceConfig(RecordsUIResourceConfig):
    template_folder = "../templates"
    url_prefix = "/oairecord/"
    blueprint_name = "oai-record-ui"
    ui_serializer_class = (
        "oarepo_oaipmh_harvester.oai_record.resources.records.ui.OaiRecordUIJSONSerializer"
    )
    api_service = "oarepo-oaipmh-record"
    layout = "oarepo_oaipmh_harvester.oai_record"

    templates = {
        "detail": {
            "layout": "oai_record_ui/detail.html",
            "blocks": {
                "record_main_content": "oai_record_ui/main.html",
                "record_sidebar": "oai_record_ui/sidebar.html",
            },
        },
        "search": {"layout": "oai_record_ui/search.html"},
    }

    routes = {
        "search": "",
        "detail": "/<pid_value>",
        "export": "/<pid_value>/export/<export_format>",
    }
    def search_active_facets(self, api_config, identity):
        return list(self.search_available_facets(api_config, identity).keys())


from oarepo_ui.resources.config import RecordsUIResourceConfig
import marshmallow as ma

class OAIHarvesterUIResourceConfig(RecordsUIResourceConfig):
    template_folder = "../templates"
    url_prefix = "/oaiharvester/"
    blueprint_name = "oai-harvester-ui"
    ui_serializer_class = (
        "oarepo_oaipmh_harvester.oai_harvester.resources.records.ui.OaiHarvesterUIJSONSerializer"
    )
    api_service = "oarepo-oaipmh-harvester"
    layout = "oarepo_oaipmh_harvester.oai_harvester"

    templates = {
        "detail": {
            "layout": "oai_harvester_ui/detail.html",
            "blocks": {
                "record_main_content": "oai_harvester_ui/main.html",
                "record_sidebar": "oai_harvester_ui/sidebar.html",
            },
        },
        "search": {"layout": "oai_harvester_ui/search.html"},
    }

    routes = {
        "search": "",
        "detail": "/<pid_value>",
        "export": "/<pid_value>/export/<export_format>",
    }

    def search_active_facets(self, api_config, identity):
        return list(self.search_available_facets(api_config, identity).keys())


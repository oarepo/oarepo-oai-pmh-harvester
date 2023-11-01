from oarepo_ui.resources.config import RecordsUIResourceConfig


class OAIHarvesterUIResourceConfig(RecordsUIResourceConfig):
    template_folder = "../templates"
    url_prefix = "/oai/harvest/harvesters/"
    blueprint_name = "oai-harvester-ui"
    ui_serializer_class = "oarepo_oaipmh_harvester.oai_harvester.resources.records.ui.OaiHarvesterUIJSONSerializer"
    api_service = "oarepo-oaipmh-harvesters"
    layout = "oarepo-oaipmh-harvester"

    templates = {
        "detail": {
            "layout": "oai_harvester_ui/HarvesterDetail.html.jinja",
            "blocks": {
                "record_main_content": "HarvesterMain",
                "record_sidebar": "HarvesterSidebar",
            },
        },
        "search": {
            "layout": "oai_harvester_ui/HarvesterSearch.jinja",
            "app_id": "OaiHarvester.Search",
        },
    }

    routes = {
        "search": "",
        "detail": "/<pid_value>",
        "export": "/<pid_value>/export/<export_format>",
    }

    def search_active_facets(self, api_config, identity):
        return list(self.search_available_facets(api_config, identity).keys())

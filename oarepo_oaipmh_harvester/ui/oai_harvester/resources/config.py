from oarepo_ui.resources.config import RecordsUIResourceConfig


class OAIHarvesterUIResourceConfig(RecordsUIResourceConfig):
    template_folder = "../templates"
    url_prefix = "/oai/harvest/harvesters/"
    blueprint_name = "oai-harvester-ui"
    ui_serializer_class = "oarepo_oaipmh_harvester.oai_harvester.resources.records.ui.OaiHarvesterUIJSONSerializer"
    api_service = "oarepo-oaipmh-harvesters"
    layout = "oarepo-oaipmh-harvester"

    application_id = "oai_harvester_ui"

    templates = {
        "detail": "oai_harvester_ui.HarvesterDetail",
        "search": "oai_harvester_ui.HarvesterSearch",
    }

    routes = {
        "search": "",
        "detail": "/<pid_value>",
        "export": "/<pid_value>/export/<export_format>",
    }

    def search_active_facets(self, api_config, identity):
        return list(self.search_available_facets(api_config, identity).keys())

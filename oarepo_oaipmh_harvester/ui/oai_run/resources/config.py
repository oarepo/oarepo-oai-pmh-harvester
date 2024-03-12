from oarepo_ui.resources.config import RecordsUIResourceConfig


class OaiRunUIResourceConfig(RecordsUIResourceConfig):
    template_folder = "../templates"
    url_prefix = "/oai/harvest/runs/"
    blueprint_name = "oai-run-ui"
    ui_serializer_class = (
        "oarepo_oaipmh_harvester.oai_run.resources.records.ui.OaiRunUIJSONSerializer"
    )
    api_service = "oarepo-oaipmh-runs"
    layout = "oarepo-oaipmh-run"

    application_id = "oai_run_ui"

    templates = {
        "detail": "oai_run_ui.RunDetail",
        "search": "oai_run_ui.RunSearch",
    }

    routes = {
        "search": "",
        "detail": "/<pid_value>",
        "export": "/<pid_value>/export/<export_format>",
    }

    def search_active_facets(self, api_config, identity):
        return list(self.search_available_facets(api_config, identity).keys())

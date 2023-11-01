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

    templates = {
        "detail": {
            "layout": "oai_run_ui/RunDetail.jinja",
            "blocks": {
                "record_main_content": "RunMain",
                "record_sidebar": "RunSidebar",
            },
        },
        "search": {"layout": "oai_run_ui/RunSearch.jinja", "app_id": "OaiRun.Search"},
    }

    routes = {
        "search": "",
        "detail": "/<pid_value>",
        "export": "/<pid_value>/export/<export_format>",
    }

    def search_active_facets(self, api_config, identity):
        return list(self.search_available_facets(api_config, identity).keys())

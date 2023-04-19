from oarepo_ui.resources.config import RecordsUIResourceConfig



class OaiRunUIResourceConfig(RecordsUIResourceConfig):
    template_folder = "../templates"
    url_prefix = "/oairun/"
    blueprint_name = "oai-run-ui"
    ui_serializer_class = (
        "oarepo_oaipmh_harvester.oai_run.resources.records.ui.OaiRunUIJSONSerializer"
    )
    api_service = "oarepo-oaipmh-run"
    layout = "oarepo_oaipmh_harvester.oai_run"

    templates = {
        "detail": {
            "layout": "oai_run_ui/detail.html",
            "blocks": {
                "record_main_content": "oai_run_ui/main.html",
                "record_sidebar": "oai_run_ui/sidebar.html",
            },
        },
        "search": {"layout": "oai_run_ui/search.html"},
    }

    routes = {
        "search": "",
        "detail": "/<pid_value>",
        "export": "/<pid_value>/export/<export_format>",
    }

    def search_active_facets(self, api_config, identity):
        return list(self.search_available_facets(api_config, identity).keys())




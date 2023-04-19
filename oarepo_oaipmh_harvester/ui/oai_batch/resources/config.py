from oarepo_ui.resources.config import RecordsUIResourceConfig
import marshmallow as ma


class OAIBatchUIResourceConfig(RecordsUIResourceConfig):
    template_folder = "../templates"
    url_prefix = "/oaibatch/"
    blueprint_name = "oai-batch-ui"
    ui_serializer_class = (
        "oarepo_oaipmh_harvester.oai_batch.resources.records.ui.OaiBatchUIJSONSerializer"
    )
    api_service = "oarepo-oaipmh-batch"
    layout = "oarepo_oaipmh_harvester.oai_batch"

    templates = {
        "detail": {
            "layout": "oai_batch_ui/detail.html",
            "blocks": {
                "record_main_content": "oai_batch_ui/main.html",
                "record_sidebar": "oai_batch_ui/sidebar.html",
            },
        },
        "search": {"layout": "oai_batch_ui/search.html"},
    }

    routes = {
        "search": "",
        "detail": "/<pid_value>",
        "export": "/<pid_value>/export/<export_format>",
    }

    def search_active_facets(self, api_config, identity):
        return list(self.search_available_facets(api_config, identity).keys())



from oarepo_ui.resources.config import RecordsUIResourceConfig


class OAIBatchUIResourceConfig(RecordsUIResourceConfig):
    template_folder = "../templates"
    url_prefix = "/oai/harvest/batches/"
    blueprint_name = "oai-batch-ui"
    ui_serializer_class = "oarepo_oaipmh_harvester.oai_batch.resources.records.ui.OaiBatchUIJSONSerializer"
    api_service = "oarepo-oaipmh-batches"
    layout = "oarepo-oaipmh-batch"

    templates = {
        "detail": {
            "layout": "oai_batch_ui/BatchDetail.html.jinja",
            "blocks": {
                "record_main_content": "BatchMain",
                "record_sidebar": "BatchSidebar",
            },
        },
        "search": {
            "layout": "oai_batch_ui/BatchSearch.jinja",
            "app_id": "OaiBatch.Search",
        },
    }

    routes = {
        "search": "",
        "detail": "/<pid_value>",
        "export": "/<pid_value>/export/<export_format>",
    }

    def search_active_facets(self, api_config, identity):
        return list(self.search_available_facets(api_config, identity).keys())

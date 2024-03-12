from oarepo_ui.resources.config import RecordsUIResourceConfig

from oarepo_oaipmh_harvester.ui.oai_batch.resources.components import (
    FilterErrorsComponent,
)


class OAIBatchUIResourceConfig(RecordsUIResourceConfig):
    template_folder = "../templates"
    url_prefix = "/oai/harvest/batches/"
    blueprint_name = "oai-batch-ui"
    ui_serializer_class = "oarepo_oaipmh_harvester.oai_batch.resources.records.ui.OaiBatchUIJSONSerializer"
    api_service = "oarepo-oaipmh-batches"
    layout = "oarepo-oaipmh-batch"

    application_id = "oai_batch_ui"

    templates = {
        "detail": "oai_batch_ui.BatchDetail",
        "search": "oai_batch_ui.BatchSearch",
    }

    routes = {
        "search": "",
        "detail": "/<pid_value>",
        "export": "/<pid_value>/export/<export_format>",
    }

    components = [FilterErrorsComponent]

    def search_active_facets(self, api_config, identity):
        return list(self.search_available_facets(api_config, identity).keys())

from invenio_administration.views.base import (
    AdminResourceCreateView,
    AdminResourceDetailView,
    AdminResourceEditView,
    AdminResourceListView,
    AdminView,
)
from invenio_i18n import lazy_gettext as _


class BatchListView(AdminResourceListView):
    api_endpoint = "/oai/harvest/batches/"
    extension_name = "oarepo_oaipmh_harvester.oai_batch"
    name = "batches"
    menu_label = "OAI-PMH Batches"
    resource_config = "resource_records"
    search_request_headers = {"Accept": "application/json"}
    title = "OAI-PMH Batches"
    category = "Site management"
    pid_path = "id"
    icon = "exchange"

    display_search = True
    display_delete = False
    display_create = False
    display_edit = False
    item_field_list = {
        "id": {"text": _("Id"), "order": 1},
        "status": {"text": _("Status"), "order": 2},
        "created": {"text": _("Created"), "order": 3},
        "finished": {"text": _("Finished"), "order": 4},
    }

    search_config_name = "OAI_BATCH_SEARCH"
    search_sort_config_name = "OAI_BATCH_SORT_OPTIONS"


class BatchDetailView(AdminResourceDetailView):
    url = "/batches/<pid_value>"
    api_endpoint = "/oai/harvest/batches/"
    search_request_headers = {"Accept": "application/json"}
    name = "OAI-PMH Batch detail"
    resource_config = "resource_records"
    title = "OAI-PMH Batch Detail"
    extension_name = "oarepo_oaipmh_harvester.oai_batch"

    template = "oai_harvester_ui/oai-details.html"
    display_delete = False
    display_edit = False

    list_view_name = "batches"
    pid_path = "id"

    item_field_list = {
        "id": {"text": _("Id"), "order": 1},
        "harvester.name": {"text": _("Harvester"), "order": 2},
        "created": {"text": _("Created"), "order": 3},
        "finished": {"text": _("Finished"), "order": 4},
    }

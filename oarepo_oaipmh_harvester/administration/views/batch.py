from invenio_administration.views.base import (
    AdminResourceDetailView,
    AdminResourceListView,
)
from invenio_i18n import lazy_gettext as _


class BatchListView(AdminResourceListView):
    api_endpoint = "/oai/harvest/batches/"
    extension_name = "oarepo_oaipmh_harvester.oai_batch"
    name = "oarepo_oaipmh_batches"
    url = "/oarepo/batches"
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
    url = "/oarepo/batches/<pid_value>"
    api_endpoint = "/oai/harvest/batches/"
    search_request_headers = {"Accept": "application/json"}
    name = "oarepo_oaipmh_batch_detail"
    resource_config = "resource_records"
    title = "OAI-PMH Batch Detail"
    extension_name = "oarepo_oaipmh_harvester.oai_batch"

    display_delete = False
    display_edit = False

    list_view_name = "oarepo_oaipmh_batches"
    pid_path = "id"

    item_field_list = {
        "id": {"text": _("Id"), "order": 1},
        "harvester.name": {"text": _("Harvester"), "order": 2},
        "created": {"text": _("Created"), "order": 3},
        "finished": {"text": _("Finished"), "order": 4},
    }

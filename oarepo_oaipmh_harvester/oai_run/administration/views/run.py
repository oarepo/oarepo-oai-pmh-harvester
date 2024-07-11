from invenio_administration.views.base import (
    AdminResourceDetailView,
    AdminResourceListView,
)
from invenio_i18n import lazy_gettext as _


class RunListView(AdminResourceListView):
    api_endpoint = "/oai/harvest/runs/"
    extension_name = "oarepo_oaipmh_harvester.oai_run"
    name = "runs"
    menu_label = "OAI-PMH Runs"
    resource_config = "resource_records"
    search_request_headers = {"Accept": "application/json"}
    title = "OAI-PMH Runs"
    category = "Site management"
    pid_path = "id"
    icon = "exchange"

    display_search = True
    display_delete = True
    display_create = False
    item_field_list = {
        "id": {"text": _("Id"), "order": 1},
        "created": {"text": _("Created"), "order": 2},
        "finished": {"text": _("Finished"), "order": 3},
    }

    search_config_name = "OAI_RUN_SEARCH"
    search_sort_config_name = "OAI_RUN_SORT_OPTIONS"


class RunDetailView(AdminResourceDetailView):
    url = "/runs/<pid_value>"
    api_endpoint = "/oai/harvest/runs/"
    search_request_headers = {"Accept": "application/json"}
    name = "OAI-PMH Runs detail"
    resource_config = "resource_records"
    title = "OAI-PMH Runs Detail"
    extension_name = "oarepo_oaipmh_harvester.oai_run"

    display_delete = False
    display_edit = False

    list_view_name = "runs"
    pid_path = "id"

    item_field_list = {
        "id": {"text": _("Id"), "order": 1},
        "created": {"text": _("Created"), "order": 2},
        "finished": {"text": _("Finished"), "order": 3},
    }

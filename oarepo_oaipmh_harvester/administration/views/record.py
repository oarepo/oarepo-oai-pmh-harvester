from invenio_administration.views.base import (
    AdminResourceDetailView,
    AdminResourceListView,
)
from invenio_i18n import lazy_gettext as _


class RecordListView(AdminResourceListView):
    api_endpoint = "/oai/harvest/records/"
    url = "/oarepo/records"
    extension_name = "oarepo_oaipmh_harvester.oai_record"
    name = "oarepo_oaipmh_records"
    menu_label = "OAI-PMH Records"
    resource_config = "resource_records"
    search_request_headers = {"Accept": "application/json"}
    title = "OAI-PMH Records"
    category = "Site management"
    pid_path = "id"
    icon = "exchange"

    display_search = True
    display_delete = False
    display_create = False
    display_edit = False
    item_field_list = {
        "id": {"text": _("Id"), "order": 1},
        "title": {"text": _("Title"), "order": 2},
        "created": {"text": _("Created"), "order": 3},
    }

    search_config_name = "OAI_RECORD_SEARCH"
    search_sort_config_name = "OAI_RECORD_SORT_OPTIONS"


class RecordDetailView(AdminResourceDetailView):
    url = "/oarepo/records/<pid_value>"
    api_endpoint = "/oai/harvest/records/"
    search_request_headers = {"Accept": "application/json"}
    name = "oarepo_oaipmh_record_detail"
    resource_config = "resource_records"
    title = "OAI-PMH Record Detail"
    extension_name = "oarepo_oaipmh_harvester.oai_record"

    display_delete = False
    display_edit = False

    list_view_name = "oarepo_oaipmh_records"
    pid_path = "id"

    item_field_list = {
        "id": {"text": _("Id"), "order": 2},
        "title": {"text": _("Title"), "order": 1},
        "created": {"text": _("Created"), "order": 3},
        "harvester.code": {"text": _("Harvester code"), "order": 4},
        "oai_identifier": {"text": _("OAI identifier"), "order": 5},
        "errors": {"text": _("Errors"), "order": 6},
    }

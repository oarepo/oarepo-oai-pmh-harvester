import functools

from flask_principal import UserNeed
from invenio_access.permissions import Permission
from invenio_administration.permissions import (
    administration_access_action,
)
from invenio_administration.views.base import (
    AdminResourceDetailView,
    AdminResourceListView,
)
from invenio_i18n import lazy_gettext as _

from ...oai_harvester.records.models import OaiHarvesterMetadata


def oai_record_permissions_decorator(view):
    @functools.wraps(view)
    def wrapper(*args, **kwargs):
        # get all harvesters and their managers
        manager_needs = set()
        for md in OaiHarvesterMetadata.query.all():
            for manager in (md.json or {}).get("harvest_managers", []):
                manager_needs.add(UserNeed(manager["id"]))
        oai_record_permission = Permission(administration_access_action, *manager_needs)

        return oai_record_permission.require(http_exception=403)(view)(*args, **kwargs)

    return wrapper


class OAIHarvesterPermissionsMixin:
    decorators = [oai_record_permissions_decorator]


class RecordListView(OAIHarvesterPermissionsMixin, AdminResourceListView):
    """Configuration for OAI-PMH sets list view."""

    api_endpoint = "/oai/harvest/records"
    extension_name = "oarepo_oaipmh_harvester.oai_harvester"
    name = "oarepo_oaipmh_harvest_records"
    url = "/oarepo/harvest/records"

    resource_config = "resource_records"
    search_request_headers = {"Accept": "application/vnd.inveniordm.v1+json"}
    title = "OAI-PMH Harvester Records"
    category = "Site management"
    pid_path = "id"
    icon = "exchange"
    order = 1
    menu_label = "OAI-PMH Harvester Records"

    actions = {
        "stop": {
            "text": "Stop",
            "order": 1,
            "payload_schema": None,
        }
    }

    display_search = True
    display_delete = False
    display_edit = False
    display_create = False

    item_field_list = {
        "oai_identifier": {"text": _("OAI Identifier"), "order": 1, "width": 4},
        "record_id": {"text": _("Record ID"), "order": 2},
        "datestamp": {"text": _("Datestamp"), "order": 3},
        "deleted": {"text": _("Deleted"), "order": 4},
        "has_errors": {"text": _("Has errors"), "order": 5},
    }

    search_config_name = "OAI_RECORD_SEARCH"
    search_facets_config_name = "OAI_RECORD_FACETS"
    search_sort_config_name = "OAI_RECORD_SORT_OPTIONS"


class RecordDetailView(OAIHarvesterPermissionsMixin, AdminResourceDetailView):
    """Configuration for OAI-PMH sets detail view."""

    url = "/oarepo/harvest/records/<pid_value>"
    api_endpoint = "/oai/harvest/records/"
    request_headers = {"Accept": "application/invenio-administration-detail+json"}
    name = "oarepo_oaipmh_records_detail"
    resource_config = "resource_records"
    title = "OAI-PMH Harvester Record"
    extension_name = "oarepo_oaipmh_harvester.oai_harvester"

    display_delete = False
    display_edit = False

    list_view_name = "oarepo_oaipmh_harvest_records"
    pid_path = "id"

    item_field_list = {
        "oai_identifier": {"text": _("OAI Identifier"), "order": 1, "width": 4},
        "record_id": {"text": _("Record ID"), "order": 2},
        "datestamp": {"text": _("Datestamp"), "order": 3},
        "run": {"text": _("Run"), "order": 4, "escape": True},
        "deleted": {"text": _("Deleted"), "order": 5},
        "has_errors": {"text": _("Has errors"), "order": 6},
        "errors": {"text": _("Errors"), "order": 7, "escape": True},
        "original_data": {"text": _("Original data"), "order": 8, "escape": True},
        "transformed_data": {"text": _("Transformed data"), "order": 9, "escape": True},
    }

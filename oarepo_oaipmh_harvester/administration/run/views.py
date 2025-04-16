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

from oarepo_oaipmh_harvester.oai_harvester.records.models import OaiHarvesterMetadata


def oai_run_permissions_decorator(view):
    @functools.wraps(view)
    def wrapper(*args, **kwargs):
        # get all harvesters and their managers
        manager_needs = set()
        for md in OaiHarvesterMetadata.query.all():
            for manager in (md.json or {}).get("harvest_managers", []):
                manager_needs.add(UserNeed(manager["id"]))
        oai_run_permission = Permission(administration_access_action, *manager_needs)

        return oai_run_permission.require(http_exception=403)(view)(*args, **kwargs)

    return wrapper


class OAIHarvesterPermissionsMixin:
    decorators = [oai_run_permissions_decorator]


class RunListView(OAIHarvesterPermissionsMixin, AdminResourceListView):
    """Configuration for OAI-PMH sets list view."""

    api_endpoint = "/oai/harvest/runs"
    extension_name = "oarepo_oaipmh_harvester.oai_harvester"
    name = "oarepo_oaipmh_harvest_runs"
    url = "/oarepo/harvest/runs"

    resource_config = "resource_records"
    search_request_headers = {
        "Accept": "application/invenio-administration-detail+json"
    }
    title = "OAI-PMH Harvester Runs"
    category = "Site management"
    pid_path = "id"
    icon = "exchange"
    order = 1
    menu_label = "OAI-PMH Harvester Runs"

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
        "start_time": {"text": _("Start time"), "order": 1, "width": 4},
        "end_time": {"text": _("End time"), "order": 2},
        "harvester_name": {"text": _("Harvester Name"), "order": 3},
        "title": {"text": _("Title"), "order": 4},
        "status": {"text": _("Status"), "order": 5, "width": 2},
        "records": {"text": _("Records"), "order": 6, "width": 1},
        "finished_records": {"text": _("Finished records"), "order": 7, "width": 1},
        "ok_records": {"text": _("OK records"), "order": 8, "width": 1},
        "failed_records": {"text": _("Failed records"), "order": 9, "width": 1},
    }

    search_config_name = "OAI_RUN_SEARCH"
    search_facets_config_name = "OAI_RUN_FACETS"
    search_sort_config_name = "OAI_RUN_SORT_OPTIONS"

    create_view_name = "oarepo_oaipmh_create"


class RunDetailView(OAIHarvesterPermissionsMixin, AdminResourceDetailView):
    """Configuration for OAI-PMH sets detail view."""

    url = "/oarepo/harvest/runs/<pid_value>"
    api_endpoint = "/oai/harvest/runs/"
    request_headers = {"Accept": "application/invenio-administration-detail+json"}
    name = "oarepo_oaipmh_runs_detail"
    resource_config = "resource_records"
    title = "OAI-PMH Harvester Run"
    extension_name = "oarepo_oaipmh_harvester.oai_harvester"

    display_delete = False
    display_edit = False

    list_view_name = "oarepo_oaipmh_harvest_runs"
    pid_path = "id"

    actions = {
        "stop": {
            "text": "Stop",
            "order": 1,
            "payload_schema": None,
        }
    }

    item_field_list = {
        "start_time": {"text": _("Start time"), "order": 1, "width": 4},
        "end_time": {"text": _("End time"), "order": 2},
        "harvester_name": {"text": _("Harvester Name"), "order": 3},
        "title": {"text": _("Title"), "order": 4},
        "status": {"text": _("Status"), "order": 5, "width": 2},
        "manual": {"text": _("Manual"), "order": 6, "width": 1},
        "records": {"text": _("Records"), "order": 7, "width": 1},
        "finished_records": {"text": _("Finished records"), "order": 8, "width": 1},
        "ok_records": {"text": _("OK records"), "order": 9, "width": 1},
        "failed_records": {"text": _("Failed records"), "order": 10, "width": 1},
        "records_url": {
            "text": _("Records"),
            "order": 11,
            "escape": True,
        },
    }

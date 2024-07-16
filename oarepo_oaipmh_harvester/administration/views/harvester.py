from invenio_administration.views.base import (
    AdminResourceDetailView,
    AdminResourceListView,
)
from invenio_i18n import lazy_gettext as _

from ..base import OarepoAdminFormView


class OaiPmhListView(AdminResourceListView):
    """Configuration for OAI-PMH sets list view."""

    api_endpoint = "/oai/harvest/harvesters/"
    extension_name = "oarepo_oaipmh_harvester.oai_harvester"
    name = "harvesters"

    resource_config = "resource_records"
    search_request_headers = {"Accept": "application/json"}
    title = "OAI-PMH Harvesters"
    category = "Site management"
    pid_path = "id"
    icon = "exchange"
    order = 1
    menu_label = "OAI-PMH Harvesters"

    display_search = True
    display_delete = True
    display_create = True
    display_edit = True

    item_field_list = {
        "name": {"text": _("Name"), "order": 1},
        "code": {"text": _("Code"), "order": 2},
        "baseurl": {"text": _("Base URL"), "order": 3},
        "metadataprefix": {"text": _("Metadata prefix"), "order": 4},
        "created": {"text": _("Created"), "order": 5},
    }

    search_config_name = "OAI_HARVESTER_SEARCH"
    search_sort_config_name = "OAI_HARVESTER_SORT_OPTIONS"

    create_view_name = "oaipmh_create"


class OaiPmhDetailView(AdminResourceDetailView):
    """Configuration for OAI-PMH sets detail view."""

    url = "/harvesters/<pid_value>"
    api_endpoint = "/oai/harvest/harvesters/"
    search_request_headers = {"Accept": "application/json"}
    name = "oaipmh_detail"
    resource_config = "resource_records"
    title = "OAI-PMH Harvesters"
    extension_name = "oarepo_oaipmh_harvester.oai_harvester"

    display_delete = True
    display_edit = True

    list_view_name = "harvesters"
    pid_path = "id"

    item_field_list = {
        "name": {"text": _("Name"), "order": 1},
        "code": {"text": _("Code"), "order": 2},
        "setspecs": {"text": _("Set specification"), "order": 3},
        "metadataprefix": {"text": _("Metadata prefix"), "order": 4},
        "baseurl": {"text": _("Base URL"), "order": 5},
        "loader": {"text": _("Loader"), "order": 6},
        "writer": {"text": _("Writer"), "order": 7},
        "batch_size": {"text": _("Batch size"), "order": 8},
        "max_records": {"text": _("Maximum number of records"), "order": 9},
        "transformers": {"text": _("Tranformers"), "order": 10},
        "created": {"text": _("Created"), "order": 11},
        "updated": {"text": _("Updated"), "order": 12},
        "comment": {"text": _("Comment"), "order": 13},
    }


class OaiPmhEditView(OarepoAdminFormView):
    """Configuration for OAI-PMH sets edit view."""

    name = "oaipmh_edit"
    url = "/harvesters/<pid_value>/edit"
    resource_config = "resource_records"
    pid_path = "id"
    api_endpoint = "/oai/harvest/harvesters/"
    title = "Edit OAI-PMH harvester"
    extension_name = "oarepo_oaipmh_harvester.oai_harvester"
    template = "invenio_administration/edit.html"
    list_view_name = "harvesters"

    form_fields = {
        "name": {
            "order": 1,
            "text": _("Name"),
        },
        "code": {
            "order": 2,
            "text": _("Code"),
        },
        "baseurl": {
            "order": 3,
            "text": _("Base URL"),
        },
        "metadataprefix": {
            "order": 4,
            "text": _("Metadataprefix"),
        },
        "comment": {
            "order": 5,
            "text": _("comment"),
        },
        "setspecs": {
            "order": 6,
            "text": _("Setspecs"),
        },
        "loader": {
            "order": 7,
            "text": _("loader"),
        },
        "batch_size": {
            "order": 8,
            "text": _("batch_size"),
        },
        "max_records": {
            "order": 10,
            "text": _("max_records"),
        },
        "transformers": {
            "order": 11,
            "text": _("transformers"),
            "description": _("A short human-readable string naming the set."),
            "type": "string",
        },
        "writer": {
            "order": 9,
            "text": _("writer"),
        },
    }


class OaiPmhCreateView(OarepoAdminFormView):
    """Configuration for OAI-PMH sets create view."""

    name = "oaipmh_create"
    url = "/harvesters/create"
    resource_config = "resource_records"
    pid_path = "id"
    api_endpoint = "/oai/harvest/harvesters/"
    title = "Create OAI-PMH Harvester"
    extension_name = "oarepo_oaipmh_harvester.oai_harvester"
    list_view_name = "harvesters"
    template = "invenio_administration/create.html"

    form_fields = {
        "name": {
            "order": 1,
            "text": _("Name"),
        },
        "code": {
            "order": 2,
            "text": _("Code"),
        },
        "baseurl": {
            "order": 3,
            "text": _("Base URL"),
        },
        "metadataprefix": {
            "order": 4,
            "text": _("Metadataprefix"),
        },
        "comment": {
            "order": 5,
            "text": _("comment"),
        },
        "setspecs": {
            "order": 6,
            "text": _("Set specifications"),
        },
        "loader": {
            "order": 7,
            "text": _("loader"),
        },
        "batch_size": {
            "order": 8,
            "text": _("batch_size"),
        },
        "max_records": {
            "order": 10,
            "text": _("max_records"),
        },
        "transformers": {
            "order": 8,
            "text": _("transformers"),
            "description": _("A short human-readable string naming the set."),
            "type": "string",
        },
        "writer": {
            "order": 9,
            "text": _("writer"),
        },
    }

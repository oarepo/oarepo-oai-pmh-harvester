import functools

import marshmallow as ma
from flask_principal import UserNeed
from invenio_access.permissions import Permission
from invenio_administration.permissions import (
    administration_access_action,
)
from invenio_administration.views.base import (
    AdminFormView,
    AdminResourceDetailView,
    AdminResourceListView,
)
from invenio_i18n import lazy_gettext as _

from ...oai_harvester.records.models import OaiHarvesterMetadata


def oai_harvester_permissions_decorator(view):
    @functools.wraps(view)
    def wrapper(*args, **kwargs):
        # get all harvesters and their managers
        manager_needs = set()
        for md in OaiHarvesterMetadata.query.all():
            for manager in (md.json or {}).get("harvest_managers", []):
                manager_needs.add(UserNeed(manager["id"]))
        oai_harvester_permission = Permission(
            administration_access_action, *manager_needs
        )

        return oai_harvester_permission.require(http_exception=403)(view)(
            *args, **kwargs
        )

    return wrapper


class OAIHarvesterPermissionsMixin:
    decorators = [oai_harvester_permissions_decorator]


class RunHarvestSchema(ma.Schema):
    caption = ma.fields.String(
        required=True,
        description=_("Caption for the harvest"),
    )


class OaiPmhListView(OAIHarvesterPermissionsMixin, AdminResourceListView):
    """Configuration for OAI-PMH sets list view."""

    api_endpoint = "/oai/harvest/harvesters/"
    extension_name = "oarepo_oaipmh_harvester.oai_harvester"
    name = "oarepo_oaipmh_harvesters"
    url = "/oarepo/harvesters"

    resource_config = "resource_records"
    search_request_headers = {"Accept": "application/json"}
    title = "OAI-PMH Harvesters"
    category = "Site management"
    pid_path = "id"
    icon = "exchange"
    order = 1
    menu_label = "OAI-PMH Harvesters"

    actions = {
        "harvest": {
            "text": "Run",
            "order": 1,
            "payload_schema": None,
            # "payload_schema": RunHarvestSchema,
        }
    }

    display_search = True
    display_delete = True
    display_create = True
    display_edit = True

    item_field_list = {
        "name": {"text": _("Name"), "order": 1},
        "code": {"text": _("Code"), "order": 2},
        "baseurl": {"text": _("Base URL"), "order": 3},
        "metadataprefix": {"text": _("Metadata prefix"), "order": 4},
        # commented to keep the results short
        # "created": {"text": _("Created"), "order": 5},
    }

    search_config_name = "OAI_HARVESTER_SEARCH"
    search_facets_config_name = "OAI_HARVESTER_FACETS"
    search_sort_config_name = "OAI_HARVESTER_SORT_OPTIONS"

    create_view_name = "oarepo_oaipmh_create"


class OaiPmhDetailView(OAIHarvesterPermissionsMixin, AdminResourceDetailView):
    """Configuration for OAI-PMH sets detail view."""

    url = "/oarepo/harvesters/<pid_value>"
    api_endpoint = "/oai/harvest/harvesters/"
    request_headers = {"Accept": "application/invenio-administration-detail+json"}
    name = "oarepo_oaipmh_harvesters_detail"
    resource_config = "resource_records"
    title = "OAI-PMH Harvesters"
    extension_name = "oarepo_oaipmh_harvester.oai_harvester"

    display_delete = True
    display_edit = True

    actions = {
        "harvest": {
            "text": "Run",
            "order": 1,
            "payload_schema": None,
            # "payload_schema": RunHarvestSchema,
        }
    }

    list_view_name = "oarepo_oaipmh_harvesters"
    pid_path = "id"

    item_field_list = {
        "name": {"text": _("Name"), "order": 1},
        "code": {"text": _("Code"), "order": 2},
        "runs": {"text": _("Runs"), "order": 3, "escape": True},
        "setspecs": {"text": _("Set specification"), "order": 4},
        "metadataprefix": {"text": _("Metadata prefix"), "order": 5},
        "baseurl": {"text": _("Base URL"), "order": 6},
        "loader": {"text": _("Loader"), "order": 7},
        "writers": {"text": _("Writer"), "order": 8, "escape": True},
        "batch_size": {"text": _("Batch size"), "order": 9},
        "max_records": {"text": _("Maximum number of records"), "order": 10},
        "transformers": {"text": _("Transformers"), "escape": True, "order": 11},
        "created": {"text": _("Created"), "order": 12},
        "updated": {"text": _("Updated"), "order": 13},
        "comment": {"text": _("Comment"), "order": 14},
        "harvest_managers": {
            "text": _("Harvest managers"),
            "order": 15,
            "escape": True,
        },
    }


class OAIHarvesterFormMixin:

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
        "batch_size": {
            "order": 7,
            "text": _("batch_size"),
        },
        "max_records": {
            "order": 8,
            "text": _("max_records"),
        },
        "loader": {
            "order": 9,
            "text": _("loader"),
        },
        "transformers": {
            "order": 10,
            "text": _("transformers"),
            "description": _(
                "A list of transformers, separated by commas, to use in the harvests."
            ),
        },
        "writers": {
            "order": 9,
            "text": _("writer"),
            "type": "string",
            "description": _(
                "A list of writers, separated by commas, to use in the harvests."
            ),
        },
        "harvest_managers": {
            "order": 12,
            "text": _("Harvest managers"),
            "description": _(
                "Email addresses of harvest managers separated by commas."
            ),
            "type": "string",
        },
    }

    def _schema_to_json(self, schema):
        ret = super()._schema_to_json(schema)
        # TODO: RDM13 has better support for admin fields, will need to be changed then
        ret.pop("harvest_managers", None)
        ret.pop("writers", None)
        ret["transformers"] = {
            "type": "string",
        }
        ret["writers"] = {"type": "string"}
        ret["harvest_managers"] = {"type": "string"}
        print("form schema", ret)
        return ret


class OaiPmhEditView(
    OAIHarvesterPermissionsMixin, OAIHarvesterFormMixin, AdminFormView
):  # OarepoAdminFormView):
    """Configuration for OAI-PMH sets edit view."""

    name = "oarepo_oaipmh_edit"
    url = "/oarepo/harvesters/<pid_value>/edit"
    resource_config = "resource_records"
    pid_path = "id"
    api_endpoint = "/oai/harvest/harvesters/"
    title = "Edit OAI-PMH harvester"
    extension_name = "oarepo_oaipmh_harvester.oai_harvester"
    template = "invenio_administration/edit.html"
    list_view_name = "oarepo_oaipmh_harvesters"


class OaiPmhCreateView(
    OAIHarvesterPermissionsMixin, OAIHarvesterFormMixin, AdminFormView
):
    """Configuration for OAI-PMH sets create view."""

    name = "oarepo_oaipmh_create"
    url = "/oarepo/harvesters/create"
    resource_config = "resource_records"
    pid_path = "id"
    api_endpoint = "/oai/harvest/harvesters/"
    title = "Create OAI-PMH Harvester"
    extension_name = "oarepo_oaipmh_harvester.oai_harvester"
    list_view_name = "oarepo_oaipmh_harvesters"
    template = "invenio_administration/create.html"

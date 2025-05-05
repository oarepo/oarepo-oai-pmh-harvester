from flask_principal import UserNeed
from invenio_access.models import ActionUsers
from invenio_access.permissions import system_identity
from invenio_administration.generators import (
    Administration,
    administration_access_action,
)
from invenio_records_permissions import BasePermissionPolicy, RecordPermissionPolicy
from invenio_records_permissions.generators import (
    AnyUser,
    AuthenticatedUser,
    Generator,
    SystemProcess,
)
from opensearch_dsl.query import MatchAll, MatchNone, Term

from oarepo_oaipmh_harvester.oai_harvester.proxies import (
    current_service as harvester_service,
)
from oarepo_oaipmh_harvester.oai_run.models import OAIHarvesterRun


class HarvestManager(Generator):
    def __init__(self):
        """Constructor."""
        super(Generator, self).__init__()

    def needs(self, **kwargs):
        """Enabling Needs."""
        if "record" not in kwargs:
            return []
        record = kwargs["record"]
        return [
            UserNeed(manager["id"]) for manager in record.get("harvest_managers", [])
        ]

    def query_filter(self, **kwargs):
        """Search filters."""
        identity = kwargs["identity"]
        if not identity or not identity.id:
            return MatchNone()
        return Term(**{"harvest_managers.id": identity.id})


class HarvestRunManager(Generator):
    def __init__(self):
        """Constructor."""
        super(Generator, self).__init__()

    def needs(self, **kwargs):
        """Enabling Needs."""
        if "record" not in kwargs:
            return []
        record = kwargs["record"]
        harvester_id = record.harvester_id
        harvester = harvester_service.read(system_identity, id_=harvester_id)

        return [
            UserNeed(manager["id"])
            for manager in harvester._record.get("harvest_managers", [])
        ]

    def query_filter(self, **kwargs):
        """Search filters."""
        identity = kwargs["identity"]
        if not identity or not identity.id:
            return MatchNone()
        return Term(**{"harvest_managers.id": identity.id})


class HarvestRecordManager(Generator):
    def __init__(self):
        """Constructor."""
        super(Generator, self).__init__()

    def needs(self, **kwargs):
        """Enabling Needs."""
        if "record" not in kwargs:
            return []
        record = kwargs["record"]
        run_id = record.run_id
        run = OAIHarvesterRun.query.get(run_id)

        harvester_id = run.harvester_id
        harvester = harvester_service.read(system_identity, id_=harvester_id)

        return [
            UserNeed(manager["id"])
            for manager in harvester._record.get("harvest_managers", [])
        ]

    def query_filter(self, **kwargs):
        """Search filters."""
        identity = kwargs["identity"]
        if not identity or not identity.id:
            return MatchNone()
        return Term(**{"harvest_managers": identity.id})


class AdministrationWithQueryFilter(Administration):
    def query_filter(self, **kwargs):
        identity = kwargs["identity"]
        user_ids = [need.value for need in identity.provides if need.method == "id"]
        if (
            user_ids
            and ActionUsers.query.filter(
                ActionUsers.user_id == user_ids[0],
                ActionUsers.action == administration_access_action.value,
                ActionUsers.exclude.is_(False),
            ).count()
        ):
            return MatchAll()
        else:
            return MatchNone()


class OAIHarvesterPermissions(RecordPermissionPolicy):
    """record policy for read only repository"""

    can_search = [SystemProcess(), AnyUser()]
    can_read = [SystemProcess(), AdministrationWithQueryFilter(), HarvestManager()]
    can_create = [SystemProcess(), AdministrationWithQueryFilter()]
    can_update = [SystemProcess(), AdministrationWithQueryFilter()]
    can_delete = [SystemProcess(), AdministrationWithQueryFilter()]
    can_manage = [SystemProcess(), AdministrationWithQueryFilter()]
    can_run_harvest = [
        SystemProcess(),
        AdministrationWithQueryFilter(),
        HarvestManager(),
    ]

    can_create_files = [SystemProcess(), AdministrationWithQueryFilter()]
    can_set_content_files = [SystemProcess(), AdministrationWithQueryFilter()]
    can_get_content_files = [SystemProcess(), AdministrationWithQueryFilter()]
    can_commit_files = [SystemProcess(), AdministrationWithQueryFilter()]
    can_read_files = [SystemProcess(), AdministrationWithQueryFilter()]
    can_update_files = [SystemProcess(), AdministrationWithQueryFilter()]
    can_delete_files = [SystemProcess(), AdministrationWithQueryFilter()]

    can_edit = [SystemProcess()]
    can_new_version = [SystemProcess()]
    can_search_drafts = [SystemProcess()]
    can_read_draft = [SystemProcess()]
    can_update_draft = [SystemProcess()]
    can_delete_draft = [SystemProcess()]
    can_publish = [SystemProcess()]
    can_draft_create_files = [SystemProcess()]
    can_draft_set_content_files = [SystemProcess()]
    can_draft_get_content_files = [SystemProcess()]
    can_draft_commit_files = [SystemProcess()]
    can_draft_read_files = [SystemProcess()]
    can_draft_update_files = [SystemProcess()]


class OAIRunPermissionPolicy(BasePermissionPolicy):
    """Permission policy for users and user groups."""

    can_create = [SystemProcess()]
    can_read = [SystemProcess(), AdministrationWithQueryFilter(), HarvestRunManager()]
    can_stop_harvest = [
        SystemProcess(),
        AdministrationWithQueryFilter(),
        HarvestRunManager(),
    ]
    can_search = [AuthenticatedUser(), SystemProcess()]
    can_update = [SystemProcess()]
    can_delete = [SystemProcess()]


class OAIRecordPermissionPolicy(BasePermissionPolicy):
    """Permission policy for users and user groups."""

    can_create = [SystemProcess()]
    can_read = [
        SystemProcess(),
        AdministrationWithQueryFilter(),
        HarvestRecordManager(),
    ]
    can_run_harvest = [
        SystemProcess(),
        AdministrationWithQueryFilter(),
        HarvestRecordManager(),
    ]
    can_search = [AuthenticatedUser(), SystemProcess()]
    can_update = [SystemProcess()]
    can_delete = [SystemProcess()]

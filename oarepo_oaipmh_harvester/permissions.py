from invenio_records_permissions import RecordPermissionPolicy
from invenio_records_permissions.generators import SystemProcess


from invenio_records_permissions.generators import AnyUser

class OAIHarvesterPermissions(RecordPermissionPolicy):
    """record policy for read only repository"""

    can_search = [SystemProcess(), AnyUser()]
    can_read = [SystemProcess(), AnyUser()]
    can_create = [SystemProcess()]
    can_update = [SystemProcess()]
    can_delete = [SystemProcess()]
    can_manage = [SystemProcess()]

    can_create_files = [SystemProcess()]
    can_set_content_files = [SystemProcess()]
    can_get_content_files = [SystemProcess()]
    can_commit_files = [SystemProcess()]
    can_read_files = [SystemProcess()]
    can_update_files = [SystemProcess()]
    can_delete_files = [SystemProcess()]

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

from invenio_records_permissions import RecordPermissionPolicy
from invenio_records_permissions.generators import AnyUser, SystemProcess


class NrThesesMetadataPermissionPolicy(RecordPermissionPolicy):
    """nr_theses_metadata.records.api.NrThesesMetadataRecord permissions."""

    can_search = [SystemProcess(), AnyUser()]
    can_read = [SystemProcess(), AnyUser()]
    can_create = [SystemProcess()]
    can_update = [SystemProcess()]
    can_delete = [SystemProcess()]
    can_manage = [SystemProcess()]

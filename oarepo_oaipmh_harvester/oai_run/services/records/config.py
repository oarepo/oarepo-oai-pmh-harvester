from invenio_records_resources.services import RecordLink
from invenio_records_resources.services import (
    RecordServiceConfig as InvenioRecordServiceConfig,
)
from invenio_records_resources.services import pagination_links
from invenio_records_resources.services.records.components import DataComponent
from oarepo_runtime.config.service import PermissionsPresetsConfigMixin

from oarepo_oaipmh_harvester.oai_run.records.api import OaiRunRecord
from oarepo_oaipmh_harvester.oai_run.services.records.permissions import (
    OaiRunPermissionPolicy,
)
from oarepo_oaipmh_harvester.oai_run.services.records.schema import OaiRunSchema
from oarepo_oaipmh_harvester.oai_run.services.records.search import OaiRunSearchOptions


class OaiRunServiceConfig(PermissionsPresetsConfigMixin, InvenioRecordServiceConfig):
    """OaiRunRecord service config."""

    PERMISSIONS_PRESETS = ["oai_harvester"]

    url_prefix = "/oarepo-oaipmh-harvester-oai-run/"

    base_permission_policy_cls = OaiRunPermissionPolicy

    schema = OaiRunSchema

    search = OaiRunSearchOptions

    record_cls = OaiRunRecord

    service_id = "oai_run"

    components = [
        *PermissionsPresetsConfigMixin.components,
        *InvenioRecordServiceConfig.components,
        DataComponent,
        DataComponent,
    ]

    model = "oarepo_oaipmh_harvester.oai_run"

    @property
    def links_item(self):
        return {
            "self": RecordLink("{self.url_prefix}{id}"),
        }

    @property
    def links_search(self):
        return {
            **pagination_links("{self.url_prefix}{?args*}"),
        }

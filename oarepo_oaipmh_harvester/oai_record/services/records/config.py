from invenio_records_resources.services import RecordLink
from invenio_records_resources.services import (
    RecordServiceConfig as InvenioRecordServiceConfig,
)
from invenio_records_resources.services import pagination_links
from invenio_records_resources.services.records.components import DataComponent
from oarepo_runtime.config.service import PermissionsPresetsConfigMixin
from oarepo_runtime.relations.components import CachingRelationsComponent

from oarepo_oaipmh_harvester.oai_record.records.api import OaiRecord
from oarepo_oaipmh_harvester.oai_record.services.records.permissions import (
    OaiRecordPermissionPolicy,
)
from oarepo_oaipmh_harvester.oai_record.services.records.schema import OaiRecordSchema
from oarepo_oaipmh_harvester.oai_record.services.records.search import (
    OaiRecordSearchOptions,
)


class OaiRecordServiceConfig(PermissionsPresetsConfigMixin, InvenioRecordServiceConfig):
    """OaiRecord service config."""

    PERMISSIONS_PRESETS = ["oai_harvester"]

    url_prefix = "/oai/harvest/records/"

    base_permission_policy_cls = OaiRecordPermissionPolicy

    schema = OaiRecordSchema

    search = OaiRecordSearchOptions

    record_cls = OaiRecord

    service_id = "oarepo-oaipmh-records"

    components = [
        *PermissionsPresetsConfigMixin.components,
        *InvenioRecordServiceConfig.components,
        CachingRelationsComponent,
        DataComponent,
    ]

    model = "oarepo_oaipmh_harvester.oai_record"

    @property
    def links_item(self):
        return {
            "self": RecordLink("{+api}/oai/harvest/records/{id}"),
        }

    @property
    def links_search(self):
        return {
            **pagination_links("{+api}/oai/harvest/records/{?args*}"),
        }

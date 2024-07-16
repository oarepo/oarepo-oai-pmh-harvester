from invenio_records_resources.services import RecordLink
from invenio_records_resources.services import (
    RecordServiceConfig as InvenioRecordServiceConfig,
)
from invenio_records_resources.services import pagination_links
from invenio_records_resources.services.records.components import DataComponent
from oarepo_runtime.services.config.service import PermissionsPresetsConfigMixin
from oarepo_runtime.services.relations.components import CachingRelationsComponent

from oarepo_oaipmh_harvester.oai_batch.records.api import OaiBatchRecord
from oarepo_oaipmh_harvester.oai_batch.services.records.permissions import (
    OaiBatchPermissionPolicy,
)
from oarepo_oaipmh_harvester.oai_batch.services.records.results import (
    OaiBatchRecordItem,
    OaiBatchRecordList,
)
from oarepo_oaipmh_harvester.oai_batch.services.records.schema import OaiBatchSchema
from oarepo_oaipmh_harvester.oai_batch.services.records.search import (
    OaiBatchSearchOptions,
)


class OaiBatchServiceConfig(PermissionsPresetsConfigMixin, InvenioRecordServiceConfig):
    """OaiBatchRecord service config."""

    result_item_cls = OaiBatchRecordItem

    result_list_cls = OaiBatchRecordList

    PERMISSIONS_PRESETS = ["oai_harvester"]

    url_prefix = "/oai/harvest/batches/"

    base_permission_policy_cls = OaiBatchPermissionPolicy

    schema = OaiBatchSchema

    search = OaiBatchSearchOptions

    record_cls = OaiBatchRecord

    service_id = "oarepo-oaipmh-batches"

    components = [
        *PermissionsPresetsConfigMixin.components,
        *InvenioRecordServiceConfig.components,
        CachingRelationsComponent,
        DataComponent,
    ]

    model = "oarepo_oaipmh_harvester.oai_batch"

    @property
    def links_item(self):
        return {
            "self": RecordLink("{+api}/oai/harvest/batches/{id}"),
            "self_html": RecordLink("{+ui}/oai/harvest/batches/{id}"),
        }

    @property
    def links_search(self):
        return {
            **pagination_links("{+api}/oai/harvest/batches/{?args*}"),
        }

from invenio_records_resources.services import RecordLink
from invenio_records_resources.services import RecordServiceConfig
from invenio_records_resources.services import (
    RecordServiceConfig as InvenioRecordServiceConfig,
)
from invenio_records_resources.services import pagination_links
from invenio_records_resources.services.records.components import DataComponent
from oarepo_runtime.config.service import PermissionsPresetsConfigMixin

from oarepo_oaipmh_harvester.oai_batch.records.api import OaiBatchRecord
from oarepo_oaipmh_harvester.oai_batch.services.records.permissions import (
    OaiBatchPermissionPolicy,
)
from oarepo_oaipmh_harvester.oai_batch.services.records.schema import OaiBatchSchema
from oarepo_oaipmh_harvester.oai_batch.services.records.search import (
    OaiBatchSearchOptions,
)


class OaiBatchServiceConfig(PermissionsPresetsConfigMixin, RecordServiceConfig):
    """OaiBatchRecord service config."""

    url_prefix = "/oarepo-oaipmh-harvester.oai-batch/"

    PERMISSIONS_PRESETS = ["oai_harvester"]

    schema = OaiBatchSchema

    search = OaiBatchSearchOptions

    record_cls = OaiBatchRecord
    # todo should i leave this here?
    service_id = "oarepo-oaipmh-batch"

    components = [*RecordServiceConfig.components, DataComponent]

    model = "oai_batch"

    @property
    def links_item(self):
        return {
            "self": RecordLink("{self.url_prefix}{id}"),
        }

    @property
    def links_search(self):
        return pagination_links("{self.url_prefix}{?args*}")
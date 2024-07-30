from invenio_records_resources.services import RecordLink
from invenio_records_resources.services import (
    RecordServiceConfig as InvenioRecordServiceConfig,
)
from invenio_records_resources.services import pagination_links
from invenio_records_resources.services.records.components import DataComponent
from oarepo_runtime.services.config.service import PermissionsPresetsConfigMixin
from oarepo_runtime.services.relations.components import CachingRelationsComponent

from oarepo_oaipmh_harvester.oai_harvester.records.api import OaiHarvesterRecord
from oarepo_oaipmh_harvester.oai_harvester.services.records.permissions import (
    OaiHarvesterPermissionPolicy,
)
from oarepo_oaipmh_harvester.oai_harvester.services.records.results import (
    OaiHarvesterRecordItem,
    OaiHarvesterRecordList,
)
from oarepo_oaipmh_harvester.oai_harvester.services.records.schema import (
    OaiHarvesterSchema,
)
from oarepo_oaipmh_harvester.oai_harvester.services.records.search import (
    OaiHarvesterSearchOptions,
)


class OaiHarvesterServiceConfig(
    PermissionsPresetsConfigMixin, InvenioRecordServiceConfig
):
    """OaiHarvesterRecord service config."""

    result_item_cls = OaiHarvesterRecordItem

    result_list_cls = OaiHarvesterRecordList

    PERMISSIONS_PRESETS = ["oai_harvester"]

    url_prefix = "/oai/harvest/harvesters/"

    base_permission_policy_cls = OaiHarvesterPermissionPolicy

    schema = OaiHarvesterSchema

    search = OaiHarvesterSearchOptions

    record_cls = OaiHarvesterRecord

    service_id = "oarepo-oaipmh-harvesters"

    components = [
        *PermissionsPresetsConfigMixin.components,
        *InvenioRecordServiceConfig.components,
        CachingRelationsComponent,
        DataComponent,
    ]

    model = "oarepo_oaipmh_harvester.oai_harvester"

    @property
    def links_item(self):
        return {
            "self": RecordLink("{+api}/oai/harvest/harvesters/{id}"),
            "self_html": RecordLink("{+ui}/oai/harvest/harvesters/{id}"),
        }

    @property
    def links_search(self):
        return {
            **pagination_links("{+api}/oai/harvest/harvesters/{?args*}"),
        }

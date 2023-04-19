from invenio_records_resources.services import RecordLink
from invenio_records_resources.services import RecordServiceConfig
from invenio_records_resources.services import pagination_links
from invenio_records_resources.services.records.components import DataComponent
from oarepo_runtime.config.service import PermissionsPresetsConfigMixin
from oarepo_runtime.relations.components import CachingRelationsComponent

from oarepo_oaipmh_harvester.oai_run.records.api import OaiRunRecord
from oarepo_oaipmh_harvester.oai_run.services.records.schema import OaiRunSchema
from oarepo_oaipmh_harvester.oai_run.services.records.search import OaiRunSearchOptions


class OaiRunServiceConfig(PermissionsPresetsConfigMixin, RecordServiceConfig):
    """OaiRunRecord service config."""

    url_prefix = "/oarepo-oaipmh-harvester.oai-run/"

    PERMISSIONS_PRESETS = ["oai_harvester"]

    schema = OaiRunSchema

    search = OaiRunSearchOptions

    record_cls = OaiRunRecord
    service_id = "oarepo-oaipmh-run"

    components = [
        *RecordServiceConfig.components,
        DataComponent,
        CachingRelationsComponent,
    ]

    model = "oai_run"

    @property
    def links_item(self):
        return {
            "self": RecordLink("{self.url_prefix}{id}"),
        }

    @property
    def links_search(self):
        return pagination_links("{self.url_prefix}{?args*}")

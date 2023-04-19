from invenio_records_resources.services import RecordLink
from invenio_records_resources.services import RecordServiceConfig
from invenio_records_resources.services import pagination_links
from invenio_records_resources.services.records.components import DataComponent
from oarepo_runtime.config.service import PermissionsPresetsConfigMixin
from oarepo_runtime.relations.components import CachingRelationsComponent

from oarepo_oaipmh_harvester.oai_record.records.api import OaiRecordRecord
from oarepo_oaipmh_harvester.oai_record.services.records.schema import OaiRecordSchema
from oarepo_oaipmh_harvester.oai_record.services.records.search import (
    OaiRecordSearchOptions,
)


class OaiRecordServiceConfig(PermissionsPresetsConfigMixin, RecordServiceConfig):
    """OaiRecordRecord service config."""

    url_prefix = "/oarepo-oaipmh-harvester.oai-record/"

    PERMISSIONS_PRESETS = ["oai_harvester"]

    schema = OaiRecordSchema

    search = OaiRecordSearchOptions

    record_cls = OaiRecordRecord
    service_id = "oarepo-oaipmh-record"

    components = [
        *RecordServiceConfig.components,
        DataComponent,
        CachingRelationsComponent,
    ]

    model = "oai_record"

    @property
    def links_item(self):
        return {
            "self": RecordLink("{self.url_prefix}{id}"),
        }

    @property
    def links_search(self):
        return pagination_links("{self.url_prefix}{?args*}")

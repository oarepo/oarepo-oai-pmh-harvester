from invenio_records_resources.services import RecordLink
from invenio_records_resources.services import RecordServiceConfig
from invenio_records_resources.services import pagination_links
from invenio_records_resources.services.records.components import DataComponent
from oarepo_runtime.config.service import PermissionsPresetsConfigMixin
from oarepo_runtime.relations.components import CachingRelationsComponent

from oarepo_oaipmh_harvester.oai_harvester.records.api import OaiHarvesterRecord
from oarepo_oaipmh_harvester.oai_harvester.services.records.schema import (
    OaiHarvesterSchema,
)
from oarepo_oaipmh_harvester.oai_harvester.services.records.search import (
    OaiHarvesterSearchOptions,
)


class OaiHarvesterServiceConfig(PermissionsPresetsConfigMixin, RecordServiceConfig):
    """OaiHarvesterRecord service config."""

    url_prefix = "/oarepo-oaipmh-harvester.oai-harvester/"

    PERMISSIONS_PRESETS = ["oai_harvester"]


    schema = OaiHarvesterSchema

    search = OaiHarvesterSearchOptions

    record_cls = OaiHarvesterRecord
    service_id = "oarepo-oaipmh-harvester"

    components = [
        *RecordServiceConfig.components,
        DataComponent,
        CachingRelationsComponent,
    ]

    model = "oai_harvester"

    @property
    def links_item(self):
        return {
            "self": RecordLink("{self.url_prefix}{id}"),
        }

    @property
    def links_search(self):
        return pagination_links("{self.url_prefix}{?args*}")

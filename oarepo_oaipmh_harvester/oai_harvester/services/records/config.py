from invenio_records_resources.services import (
    LinksTemplate,
    RecordLink,
    pagination_links,
)
from invenio_records_resources.services.records.components import DataComponent
from oarepo_runtime.services.components import (
    CustomFieldsComponent,
    process_service_configs,
)
from oarepo_runtime.services.config import has_permission
from oarepo_runtime.services.config.service import PermissionsPresetsConfigMixin
from oarepo_runtime.services.records import pagination_links_html
from oarepo_runtime.services.relations.components import CachingRelationsComponent

from oarepo_oaipmh_harvester.common.services.oai_harvester import (
    BaseOaiHarvesterServiceConfig,
)
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
    PermissionsPresetsConfigMixin, BaseOaiHarvesterServiceConfig
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
    indexer_queue_name = "oarepo-oaipmh-harvesters"

    search_item_links_template = LinksTemplate

    @property
    def components(self):
        return process_service_configs(
            self, CachingRelationsComponent, DataComponent, CustomFieldsComponent
        )

    model = "oarepo_oaipmh_harvester.oai_harvester"

    @property
    def links_item(self):
        try:
            supercls_links = super().links_item
        except AttributeError:  # if they aren't defined in the superclass
            supercls_links = {}
        links = {
            **supercls_links,
            "self": RecordLink(
                "{+api}/oai/harvest/harvesters/{id}", when=has_permission("read")
            ),
            "self_html": RecordLink(
                "{+ui}/oai/harvest/harvesters/{id}", when=has_permission("read")
            ),
        }
        return {k: v for k, v in links.items() if v is not None}

    @property
    def links_search_item(self):
        try:
            supercls_links = super().links_search_item
        except AttributeError:  # if they aren't defined in the superclass
            supercls_links = {}
        links = {
            **supercls_links,
            "self": RecordLink(
                "{+api}/oai/harvest/harvesters/{id}", when=has_permission("read")
            ),
            "self_html": RecordLink(
                "{+ui}/oai/harvest/harvesters/{id}", when=has_permission("read")
            ),
            "harvest": RecordLink(
                "{+api}/oai/harvest/harvesters/{id}/actions/harvest",
                when=has_permission("run_harvest"),
            ),
        }
        return {k: v for k, v in links.items() if v is not None}

    @property
    def links_search(self):
        try:
            supercls_links = super().links_search
        except AttributeError:  # if they aren't defined in the superclass
            supercls_links = {}
        links = {
            **supercls_links,
            **pagination_links("{+api}/oai/harvest/harvesters/{?args*}"),
            **pagination_links_html("{+ui}/oai/harvest/harvesters/{?args*}"),
        }
        return {k: v for k, v in links.items() if v is not None}

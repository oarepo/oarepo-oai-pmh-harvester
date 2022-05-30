from invenio_records_resources.services import RecordLink
from invenio_records_resources.services import \
    RecordServiceConfig as InvenioRecordServiceConfig
from invenio_records_resources.services import pagination_links
from invenio_records_resources.services.records.components import (
    DataComponent, MetadataComponent)
from oaipmh_config.records.api import OaipmhConfigRecord
from oaipmh_config.services.permissions import OaipmhConfigPermissionPolicy
from oaipmh_config.services.schema import OaipmhConfigSchema
from oaipmh_config.services.search import OaipmhConfigSearchOptions


class OaipmhConfigServiceConfig(InvenioRecordServiceConfig):
    """OaipmhConfigRecord service config."""

    permission_policy_cls = OaipmhConfigPermissionPolicy
    schema = OaipmhConfigSchema
    search = OaipmhConfigSearchOptions
    record_cls = OaipmhConfigRecord

    
    components = [ *InvenioRecordServiceConfig.components ]
    

    model = "oaipmh_config"

    @property
    def links_item(self):
        return {
            "self": RecordLink("/oaipmh_config/{id}"),
        }

    links_search = pagination_links("/oaipmh_config/{?args*}")
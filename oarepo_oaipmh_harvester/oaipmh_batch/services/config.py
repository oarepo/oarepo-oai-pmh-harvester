from invenio_records_resources.services import RecordLink
from invenio_records_resources.services import \
    RecordServiceConfig as InvenioRecordServiceConfig
from invenio_records_resources.services import pagination_links
from oarepo_oaipmh_harvester.oaipmh_batch.records.api import OaipmhBatchRecord
from oarepo_oaipmh_harvester.oaipmh_batch.services.permissions import OaipmhBatchPermissionPolicy
from oarepo_oaipmh_harvester.oaipmh_batch.services.schema import OaipmhBatchSchema
from oarepo_oaipmh_harvester.oaipmh_batch.services.search import OaipmhBatchSearchOptions


class OaipmhBatchServiceConfig(InvenioRecordServiceConfig):
    """OaipmhBatchRecord service config."""

    permission_policy_cls = OaipmhBatchPermissionPolicy
    schema = OaipmhBatchSchema
    search = OaipmhBatchSearchOptions
    record_cls = OaipmhBatchRecord

    
    components = [ *InvenioRecordServiceConfig.components ]
    

    model = "oaipmh_batch"

    @property
    def links_item(self):
        return {
            "self": RecordLink("/oaipmh_batch/{id}"),
        }

    links_search = pagination_links("/oaipmh_batch/{?args*}")
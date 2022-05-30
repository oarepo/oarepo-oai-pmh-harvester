from invenio_records_resources.services import RecordLink
from invenio_records_resources.services import \
    RecordServiceConfig as InvenioRecordServiceConfig
from invenio_records_resources.services import pagination_links
from oarepo_oaipmh_harvester.oaipmh_run.records.api import OaipmhRunRecord
from oarepo_oaipmh_harvester.oaipmh_run.services.permissions import OaipmhRunPermissionPolicy
from oarepo_oaipmh_harvester.oaipmh_run.services.schema import OaipmhRunSchema
from oarepo_oaipmh_harvester.oaipmh_run.services.search import OaipmhRunSearchOptions


class OaipmhRunServiceConfig(InvenioRecordServiceConfig):
    """OaipmhRunRecord service config."""

    permission_policy_cls = OaipmhRunPermissionPolicy
    schema = OaipmhRunSchema
    search = OaipmhRunSearchOptions
    record_cls = OaipmhRunRecord

    
    components = [ *InvenioRecordServiceConfig.components ]
    

    model = "oaipmh_run"

    @property
    def links_item(self):
        return {
            "self": RecordLink("/oaipmh_run/{id}"),
        }

    links_search = pagination_links("/oaipmh_run/{?args*}")
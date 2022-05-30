from invenio_records_resources.services import RecordLink
from invenio_records_resources.services import \
    RecordServiceConfig as InvenioRecordServiceConfig
from invenio_records_resources.services import pagination_links
from invenio_records_resources.services.records.components import (
    DataComponent, MetadataComponent)
from oaipmh_record.records.api import OaipmhRecordRecord
from oaipmh_record.services.permissions import OaipmhRecordPermissionPolicy
from oaipmh_record.services.schema import OaipmhRecordSchema
from oaipmh_record.services.search import OaipmhRecordSearchOptions


class OaipmhRecordServiceConfig(InvenioRecordServiceConfig):
    """OaipmhRecordRecord service config."""

    permission_policy_cls = OaipmhRecordPermissionPolicy
    schema = OaipmhRecordSchema
    search = OaipmhRecordSearchOptions
    record_cls = OaipmhRecordRecord

    
    components = [ *InvenioRecordServiceConfig.components ]
    

    model = "oaipmh_record"

    @property
    def links_item(self):
        return {
            "self": RecordLink("/oaipmh_record/{id}"),
        }

    links_search = pagination_links("/oaipmh_record/{?args*}")
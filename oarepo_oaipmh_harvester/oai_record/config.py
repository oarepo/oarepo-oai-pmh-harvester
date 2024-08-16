from oarepo_oaipmh_harvester.oai_record.records.api import OaiRecord
from oarepo_oaipmh_harvester.oai_record.resources.records.config import (
    OaiRecordResourceConfig,
)
from oarepo_oaipmh_harvester.oai_record.resources.records.resource import (
    OaiRecordResource,
)
from oarepo_oaipmh_harvester.oai_record.services.records.config import (
    OaiRecordServiceConfig,
)
from oarepo_oaipmh_harvester.oai_record.services.records.service import OaiRecordService

OAI_RECORD_RECORD_RESOURCE_CONFIG = OaiRecordResourceConfig


OAI_RECORD_RECORD_RESOURCE_CLASS = OaiRecordResource


OAI_RECORD_RECORD_SERVICE_CONFIG = OaiRecordServiceConfig


OAI_RECORD_RECORD_SERVICE_CLASS = OaiRecordService


OAREPO_PRIMARY_RECORD_SERVICE = {OaiRecord: "oarepo-oaipmh-records"}

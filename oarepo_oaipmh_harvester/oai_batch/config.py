from oarepo_oaipmh_harvester.oai_batch.records.api import OaiBatchRecord
from oarepo_oaipmh_harvester.oai_batch.resources.records.config import (
    OaiBatchResourceConfig,
)
from oarepo_oaipmh_harvester.oai_batch.resources.records.resource import (
    OaiBatchResource,
)
from oarepo_oaipmh_harvester.oai_batch.services.records.config import (
    OaiBatchServiceConfig,
)
from oarepo_oaipmh_harvester.oai_batch.services.records.service import OaiBatchService

OAI_BATCH_RECORD_RESOURCE_CONFIG = OaiBatchResourceConfig


OAI_BATCH_RECORD_RESOURCE_CLASS = OaiBatchResource


OAI_BATCH_RECORD_SERVICE_CONFIG = OaiBatchServiceConfig


OAI_BATCH_RECORD_SERVICE_CLASS = OaiBatchService


OAREPO_PRIMARY_RECORD_SERVICE = {OaiBatchRecord: "oarepo-oaipmh-batches"}

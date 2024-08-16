from oarepo_oaipmh_harvester.oai_run.records.api import OaiRunRecord
from oarepo_oaipmh_harvester.oai_run.resources.records.config import (
    OaiRunResourceConfig,
)
from oarepo_oaipmh_harvester.oai_run.resources.records.resource import OaiRunResource
from oarepo_oaipmh_harvester.oai_run.services.records.config import OaiRunServiceConfig
from oarepo_oaipmh_harvester.oai_run.services.records.service import OaiRunService

OAI_RUN_RECORD_RESOURCE_CONFIG = OaiRunResourceConfig


OAI_RUN_RECORD_RESOURCE_CLASS = OaiRunResource


OAI_RUN_RECORD_SERVICE_CONFIG = OaiRunServiceConfig


OAI_RUN_RECORD_SERVICE_CLASS = OaiRunService


OAREPO_PRIMARY_RECORD_SERVICE = {OaiRunRecord: "oarepo-oaipmh-runs"}

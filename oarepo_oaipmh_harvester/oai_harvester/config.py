from oarepo_oaipmh_harvester.oai_harvester.records.api import OaiHarvesterRecord
from oarepo_oaipmh_harvester.oai_harvester.resources.records.config import (
    OaiHarvesterResourceConfig,
)
from oarepo_oaipmh_harvester.oai_harvester.resources.records.resource import (
    OaiHarvesterResource,
)
from oarepo_oaipmh_harvester.oai_harvester.services.records.config import (
    OaiHarvesterServiceConfig,
)
from oarepo_oaipmh_harvester.oai_harvester.services.records.service import (
    OaiHarvesterService,
)

OAI_HARVESTER_RECORD_RESOURCE_CONFIG = OaiHarvesterResourceConfig


OAI_HARVESTER_RECORD_RESOURCE_CLASS = OaiHarvesterResource


OAI_HARVESTER_RECORD_SERVICE_CONFIG = OaiHarvesterServiceConfig


OAI_HARVESTER_RECORD_SERVICE_CLASS = OaiHarvesterService


OAREPO_PRIMARY_RECORD_SERVICE = {OaiHarvesterRecord: "oarepo-oaipmh-harvesters"}

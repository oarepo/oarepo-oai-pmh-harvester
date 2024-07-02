from oarepo_oaipmh_harvester.oai_harvester.resources.records.config import (
    OaiHarvesterResourceConfig,
)
from oarepo_oaipmh_harvester.oai_harvester.resources.records.resource import (
    OaiHarvesterResource,
)
from oarepo_oaipmh_harvester.oai_harvester.services.records import facets
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


OAI_HARVESTER_SEARCH = {
    "facets": [],
    "sort": ["newest"],
    "sort_default": "newest",
    "sort_default_no_query": "newest",
}
from invenio_i18n import lazy_gettext as _

OAI_HARVESTER_FACETS = {
    "batch_size": facets.batch_size,
    "loader": facets.loader,
    "max_records": facets.max_records,
    "metadataprefix": facets.metadataprefix,
    "setspecs": facets.setspecs,
    "transformers": facets.transformers,
}

OAI_HARVESTER_SORT_OPTIONS = {
    "newest": dict(
        title=_("Newest"),
        fields=["-created"],
    ),
}

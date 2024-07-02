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

from invenio_i18n import lazy_gettext as _

OAI_RUN_SEARCH ={
    "facets": [],
    "sort": ["newest"],
    "sort_default": "newest",
    "sort_default_no_query": "newest"
}
OAI_RUN_SORT_OPTIONS = {"newest": dict(
            title=_("Newest"),
            fields=["-created"],
        ),}
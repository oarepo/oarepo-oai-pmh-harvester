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

from invenio_i18n import lazy_gettext as _

OAI_BATCH_SEARCH = {
    "facets": [],
    "sort": ["newest"],
    "sort_default": "newest",
    "sort_default_no_query": "newest",
}

OAI_BATCH_SORT_OPTIONS = {
    "newest": dict(
        title=_("Newest"),
        fields=["-created"],
    ),
}

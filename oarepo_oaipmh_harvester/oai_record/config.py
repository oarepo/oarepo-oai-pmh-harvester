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

from invenio_i18n import lazy_gettext as _

OAI_RECORD_SEARCH = {
    "facets": [],
    "sort": ["newest"],
    "sort_default": "newest",
    "sort_default_no_query": "newest",
}
OAI_RECORD_SORT_OPTIONS = {
    "newest": dict(
        title=_("Newest"),
        fields=["-created"],
    ),
}

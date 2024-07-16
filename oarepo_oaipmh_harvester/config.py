from invenio_i18n import lazy_gettext as _

from oarepo_oaipmh_harvester.permissions import OAIHarvesterPermissions
from oarepo_oaipmh_harvester.readers.oai_dir import OAIDirReader
from oarepo_oaipmh_harvester.readers.sickle import SickleReader
from oarepo_oaipmh_harvester.transformers.marcxml import MarcXMLTransformer
from oarepo_oaipmh_harvester.transformers.record_lookup import (
    OAIRecordLookupTransformer,
)
from oarepo_oaipmh_harvester.writers.oai import OAIWriter
from oarepo_oaipmh_harvester.writers.oai_dir import OAIDirWriter

DATASTREAMS_READERS = {"sickle": SickleReader, "oai_dir": OAIDirReader}

DATASTREAMS_TRANSFORMERS = {
    "marcxml": MarcXMLTransformer,
    "oai_record_lookup": OAIRecordLookupTransformer,
}

DATASTREAMS_WRITERS = {"oai_dir": OAIDirWriter, "oai": OAIWriter}

OAREPO_PERMISSIONS_PRESETS = {"oai_harvester": OAIHarvesterPermissions}


OAI_RUN_SEARCH = {
    "facets": [],
    "sort": ["newest"],
    "sort_default": "newest",
    "sort_default_no_query": "newest",
}
OAI_RUN_SORT_OPTIONS = {
    "newest": dict(
        title=_("Newest"),
        fields=["-created"],
    ),
}

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

OAI_HARVESTER_SORT_OPTIONS = {
    "newest": dict(
        title=_("Newest"),
        fields=["-created"],
    ),
}

OAI_HARVESTER_SEARCH = {
    "facets": [],
    "sort": ["newest"],
    "sort_default": "newest",
    "sort_default_no_query": "newest",
}

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

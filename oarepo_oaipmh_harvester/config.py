from typing import Any

from invenio_i18n import lazy_gettext as _
from oarepo_runtime.datastreams import BaseReader, BaseTransformer, BaseWriter

from oarepo_oaipmh_harvester.permissions import OAIHarvesterPermissions
from oarepo_oaipmh_harvester.readers.oai_dir import OAIDirReader
from oarepo_oaipmh_harvester.readers.sickle import SickleReader
from oarepo_oaipmh_harvester.transformers.marcxml import MarcXMLTransformer
from oarepo_oaipmh_harvester.transformers.record_lookup import (
    OAIRecordLookupTransformer,
)
from oarepo_oaipmh_harvester.writers.oai import OAIWriter
from oarepo_oaipmh_harvester.writers.oai_dir import OAIDirWriter

DATASTREAMS_READERS: dict[str, type[BaseReader]] = {
    "sickle": SickleReader,
    "oai_dir": OAIDirReader,
}

DATASTREAMS_TRANSFORMERS: dict[str, type[BaseTransformer]] = {
    "marcxml": MarcXMLTransformer,
    "oai_record_lookup": OAIRecordLookupTransformer,
}

DATASTREAMS_WRITERS: dict[str, type[BaseWriter]] = {
    "oai_dir": OAIDirWriter,
    "oai": OAIWriter,
}

OAREPO_PERMISSIONS_PRESETS = {"oai_harvester": OAIHarvesterPermissions}


OAI_RUN_SEARCH: dict[str, Any] = {
    "facets": [],
    "sort": ["newest"],
    "sort_default": "newest",
    "sort_default_no_query": "newest",
}
OAI_RUN_SORT_OPTIONS: dict[str, Any] = {
    "newest": dict(
        title=_("Newest"),
        fields=["-created"],
    ),
}

OAI_BATCH_SEARCH: dict[str, Any] = {
    "facets": [],
    "sort": ["newest"],
    "sort_default": "newest",
    "sort_default_no_query": "newest",
}

OAI_BATCH_SORT_OPTIONS: dict[str, Any] = {
    "newest": dict(
        title=_("Newest"),
        fields=["-created"],
    ),
}

OAI_HARVESTER_SORT_OPTIONS: dict[str, Any] = {
    "newest": dict(
        title=_("Newest"),
        fields=["-created"],
    ),
}

OAI_HARVESTER_SEARCH: dict[str, Any] = {
    "facets": [],
    "sort": ["newest"],
    "sort_default": "newest",
    "sort_default_no_query": "newest",
}

OAI_RECORD_SEARCH: dict[str, Any] = {
    "facets": [],
    "sort": ["newest"],
    "sort_default": "newest",
    "sort_default_no_query": "newest",
}

OAI_RECORD_SORT_OPTIONS: dict[str, Any] = {
    "newest": dict(
        title=_("Newest"),
        fields=["-created"],
    ),
}

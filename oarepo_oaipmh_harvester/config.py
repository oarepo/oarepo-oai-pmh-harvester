from oarepo_oaipmh_harvester.permissions import OAIHarvesterPermissions
from oarepo_oaipmh_harvester.readers.oai_dir import OAIDirReader
from oarepo_oaipmh_harvester.readers.sickle import SickleReader
from oarepo_oaipmh_harvester.transformers.batch import OAIBatchTransformer
from oarepo_oaipmh_harvester.transformers.marcxml import MarcXMLTransformer
from oarepo_oaipmh_harvester.writers.oai import OAIWriter
from oarepo_oaipmh_harvester.writers.oai_dir import OAIDirWriter

DEFAULT_DATASTREAMS_READERS = {"sickle": SickleReader, "oai_dir": OAIDirReader}

DEFAULT_DATASTREAMS_TRANSFORMERS = {
    "marcxml": MarcXMLTransformer,
    "oai_batch": OAIBatchTransformer,
}

DEFAULT_DATASTREAMS_WRITERS = {"oai_dir": OAIDirWriter, "oai": OAIWriter}

OAREPO_PERMISSIONS_PRESETS = {"oai_harvester": OAIHarvesterPermissions}


OAREPO_OAIPMH_HARVESTER_LOADERS = {}
DEFAULT_OAREPO_OAIPMH_HARVESTER_LOADERS = {
    "sickle": {"reader": "sickle"},
    "oai_dir": {"reader": "oai_dir"},
}

OAREPO_OAIPMH_HARVESTER_TRANSFORMERS = {}
DEFAULT_OAREPO_OAIPMH_HARVESTER_TRANSFORMERS = {
    "marcxml": {"transformer": "marcxml"},
    "oai_batch": {"transformer": "oai_batch"},
}

OAREPO_OAIPMH_HARVESTER_WRITERS = {}
DEFAULT_OAREPO_OAIPMH_HARVESTER_WRITERS = {
    "oai_dir": {"writer": "oai_dir"},
    "oai": {"writer": "oai"},
    "service": {"writer": "service"},
}

from invenio_records_resources.services import SearchOptions as InvenioSearchOptions

from . import facets


class OaiRunSearchOptions(InvenioSearchOptions):
    """OaiRunRecord search options."""

    facets = {
        "harvester_id": facets.harvester_id,
        "harvester_code": facets.harvester_code,
        "harvester_baseurl": facets.harvester_baseurl,
        "harvester_metadataprefix": facets.harvester_metadataprefix,
        "harvester_name": facets.harvester_name,
        "harvester_setspecs": facets.harvester_setspecs,
        "harvester_loader": facets.harvester_loader,
        "harvester_transformers": facets.harvester_transformers,
        "harvester_writer": facets.harvester_writer,
        "harvester_max_records": facets.harvester_max_records,
        "harvester_batch_size": facets.harvester_batch_size,
        "harvester_created": facets.harvester_created,
        "harvester_updated": facets.harvester_updated,
        "harvester__schema": facets.harvester__schema,
        "batches": facets.batches,
        "status": facets.status,
        "warning": facets.warning,
        "error": facets.error,
        "started": facets.started,
        "finished": facets.finished,
        "duration": facets.duration,
        "_id": facets._id,
        "created": facets.created,
        "updated": facets.updated,
        "_schema": facets._schema,
    }
    sort_options = {
        **InvenioSearchOptions.sort_options,
    }

from invenio_records_resources.services import SearchOptions as InvenioSearchOptions

from . import facets


class OaiRunSearchOptions(InvenioSearchOptions):
    """OaiRunRecord search options."""

    facet_groups = {}

    facets = {
        "_schema": facets._schema,
        "batches": facets.batches,
        "created": facets.created,
        "duration": facets.duration,
        "error": facets.error,
        "finished": facets.finished,
        "harvester_id": facets.harvester_id,
        "harvester_code": facets.harvester_code,
        "harvester__version": facets.harvester__version,
        "_id": facets._id,
        "manual": facets.manual,
        "started": facets.started,
        "status": facets.status,
        "updated": facets.updated,
        "warning": facets.warning,
        **getattr(InvenioSearchOptions, "facets", {}),
    }

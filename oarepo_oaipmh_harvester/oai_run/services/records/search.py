from invenio_records_resources.services import SearchOptions as InvenioSearchOptions

from . import facets


class OaiRunSearchOptions(InvenioSearchOptions):
    """OaiRunRecord search options."""

    facet_groups = {}

    facets = {
        "_schema": facets._schema,
        "created": facets.created,
        "created_batches": facets.created_batches,
        "duration": facets.duration,
        "errors": facets.errors,
        "finished": facets.finished,
        "finished_batches": facets.finished_batches,
        "harvester_id": facets.harvester_id,
        "harvester_code": facets.harvester_code,
        "harvester__version": facets.harvester__version,
        "_id": facets._id,
        "manual": facets.manual,
        "started": facets.started,
        "status": facets.status,
        "title": facets.title,
        "total_batches": facets.total_batches,
        "updated": facets.updated,
        "warnings": facets.warnings,
        **getattr(InvenioSearchOptions, "facets", {}),
    }

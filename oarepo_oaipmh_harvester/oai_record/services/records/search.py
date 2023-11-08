from invenio_records_resources.services import SearchOptions as InvenioSearchOptions

from . import facets


class OaiRecordSearchOptions(InvenioSearchOptions):
    """OaiRecord search options."""

    facet_groups = {}

    facets = {
        "_schema": facets._schema,
        "batch_id": facets.batch_id,
        "batch__version": facets.batch__version,
        "created": facets.created,
        "datestamp": facets.datestamp,
        "errors_code": facets.errors_code,
        "errors_location": facets.errors_location,
        "errors_message": facets.errors_message,
        "harvester_id": facets.harvester_id,
        "harvester_writer": facets.harvester_writer,
        "harvester__version": facets.harvester__version,
        "_id": facets._id,
        "local_identifier": facets.local_identifier,
        "manual": facets.manual,
        "oai_identifier": facets.oai_identifier,
        "run_id": facets.run_id,
        "run__version": facets.run__version,
        "status": facets.status,
        "title": facets.title,
        "updated": facets.updated,
        "warnings": facets.warnings,
        **getattr(InvenioSearchOptions, "facets", {}),
    }

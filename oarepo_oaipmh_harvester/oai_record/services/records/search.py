from invenio_records_resources.services import SearchOptions as InvenioSearchOptions

from . import facets


class OaiRecordSearchOptions(InvenioSearchOptions):
    """OaiRecord search options."""

    facets = {
        "_schema": facets._schema,
        "batch_id": facets.batch_id,
        "batch__version": facets.batch__version,
        "created": facets.created,
        "datestamp": facets.datestamp,
        "errors_error_message": facets.errors_error_message,
        "errors_error_type": facets.errors_error_type,
        "harvester_id": facets.harvester_id,
        "harvester__version": facets.harvester__version,
        "_id": facets._id,
        "local_identifier": facets.local_identifier,
        "manual": facets.manual,
        "oai_identifier": facets.oai_identifier,
        "status": facets.status,
        "updated": facets.updated,
        "warnings": facets.warnings,
    }
    sort_options = {
        **InvenioSearchOptions.sort_options,
    }

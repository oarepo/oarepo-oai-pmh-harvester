from invenio_records_resources.services import SearchOptions as InvenioSearchOptions

from . import facets


class OaiBatchSearchOptions(InvenioSearchOptions):
    """OaiBatchRecord search options."""

    facets = {
        "_schema": facets._schema,
        "created": facets.created,
        "errors_error_message": facets.errors_error_message,
        "errors_error_type": facets.errors_error_type,
        "errors_oai_identifier": facets.errors_oai_identifier,
        "finished": facets.finished,
        "_id": facets._id,
        "identifiers": facets.identifiers,
        "manual": facets.manual,
        "run_id": facets.run_id,
        "run__version": facets.run__version,
        "started": facets.started,
        "status": facets.status,
        "updated": facets.updated,
    }
    sort_options = {
        **InvenioSearchOptions.sort_options,
    }

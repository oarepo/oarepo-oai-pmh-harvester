from invenio_records_resources.services import SearchOptions as InvenioSearchOptions

from . import facets


class OaiBatchSearchOptions(InvenioSearchOptions):
    """OaiBatchRecord search options."""

    facets = {
        "run_id": facets.run_id,
        "run__version": facets.run__version,
        "status": facets.status,
        "identifiers": facets.identifiers,
        "errors_oai_identifier": facets.errors_oai_identifier,
        "errors_error_keyword": facets.errors_error_keyword,
        "started": facets.started,
        "finished": facets.finished,
        "_id": facets._id,
        "created": facets.created,
        "updated": facets.updated,
        "_schema": facets._schema,
    }
    sort_options = {
        **InvenioSearchOptions.sort_options,
    }

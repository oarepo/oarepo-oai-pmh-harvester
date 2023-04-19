from invenio_records_resources.services import SearchOptions as InvenioSearchOptions

from . import facets


class OaiRecordSearchOptions(InvenioSearchOptions):
    """OaiRecordRecord search options."""

    facets = {
        "batch_id": facets.batch_id,
        "batch__version": facets.batch__version,
        "local_identifier": facets.local_identifier,
        "oai_identifier": facets.oai_identifier,
        "datestamp": facets.datestamp,
        "status": facets.status,
        "warnings_keyword": facets.warnings_keyword,
        "errors_keyword": facets.errors_keyword,
        "_id": facets._id,
        "created": facets.created,
        "updated": facets.updated,
        "_schema": facets._schema,
    }
    sort_options = {
        **InvenioSearchOptions.sort_options,
    }

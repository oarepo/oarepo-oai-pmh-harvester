from invenio_records_resources.services import SearchOptions as InvenioSearchOptions

from . import facets


class OaiHarvesterSearchOptions(InvenioSearchOptions):
    """OaiHarvesterRecord search options."""

    facets = {
        "code": facets.code,
        "baseurl": facets.baseurl,
        "metadataprefix": facets.metadataprefix,
        "name": facets.name,
        "setspecs": facets.setspecs,
        "loader": facets.loader,
        "transformers": facets.transformers,
        "writer": facets.writer,
        "max_records": facets.max_records,
        "batch_size": facets.batch_size,
        "_id": facets._id,
        "created": facets.created,
        "updated": facets.updated,
        "_schema": facets._schema,
    }
    sort_options = {
        **InvenioSearchOptions.sort_options,
    }

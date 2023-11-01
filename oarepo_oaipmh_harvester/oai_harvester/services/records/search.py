from invenio_records_resources.services import SearchOptions as InvenioSearchOptions

from . import facets


class OaiHarvesterSearchOptions(InvenioSearchOptions):
    """OaiHarvesterRecord search options."""

    facet_groups = {}

    facets = {
        "_schema": facets._schema,
        "baseurl": facets.baseurl,
        "batch_size": facets.batch_size,
        "code": facets.code,
        "created": facets.created,
        "_id": facets._id,
        "loader": facets.loader,
        "max_records": facets.max_records,
        "metadataprefix": facets.metadataprefix,
        "name": facets.name,
        "setspecs": facets.setspecs,
        "transformers": facets.transformers,
        "updated": facets.updated,
        "writer": facets.writer,
        **getattr(InvenioSearchOptions, "facets", {}),
    }

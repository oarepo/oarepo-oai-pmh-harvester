from invenio_records_resources.services import SearchOptions as InvenioSearchOptions

from . import facets


class OaiHarvesterSearchOptions(InvenioSearchOptions):
    """OaiHarvesterRecord search options."""

    facet_groups = {}

    facets = {
        "batch_size": facets.batch_size,
        "loader": facets.loader,
        "max_records": facets.max_records,
        "metadataprefix": facets.metadataprefix,
        "setspecs": facets.setspecs,
        "transformers": facets.transformers,
        **getattr(InvenioSearchOptions, "facets", {}),
    }

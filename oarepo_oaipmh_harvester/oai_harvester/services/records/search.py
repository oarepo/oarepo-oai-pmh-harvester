from oarepo_runtime.services.search import SearchOptions

from . import facets


class OaiHarvesterSearchOptions(SearchOptions):
    """OaiHarvesterRecord search options."""

    facet_groups = {}

    facets = {
        "batch_size": facets.batch_size,
        "loader": facets.loader,
        "max_records": facets.max_records,
        "metadataprefix": facets.metadataprefix,
        "setspecs": facets.setspecs,
        "transformers": facets.transformers,
        "writers": facets.writers,
        **getattr(SearchOptions, "facets", {}),
    }

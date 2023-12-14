from oarepo_runtime.services.search import SearchOptions

from . import facets


class OaiRunSearchOptions(SearchOptions):
    """OaiRunRecord search options."""

    facet_groups = {}

    facets = {
        "harvester_name": facets.harvester_name,
        "manual": facets.manual,
        "status": facets.status,
        **getattr(SearchOptions, "facets", {}),
    }

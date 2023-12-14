from oarepo_runtime.services.search import SearchOptions

from . import facets


class OaiBatchSearchOptions(SearchOptions):
    """OaiBatchRecord search options."""

    facet_groups = {}

    facets = {
        "harvester_name": facets.harvester_name,
        "manual": facets.manual,
        "records_errors_code": facets.records_errors_code,
        "status": facets.status,
        **getattr(SearchOptions, "facets", {}),
    }

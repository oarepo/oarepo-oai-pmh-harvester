from invenio_records_resources.services import SearchOptions as InvenioSearchOptions

from . import facets


class OaiBatchSearchOptions(InvenioSearchOptions):
    """OaiBatchRecord search options."""

    facet_groups = {}

    facets = {
        "harvester_name": facets.harvester_name,
        "manual": facets.manual,
        "records_errors_code": facets.records_errors_code,
        "status": facets.status,
        **getattr(InvenioSearchOptions, "facets", {}),
    }

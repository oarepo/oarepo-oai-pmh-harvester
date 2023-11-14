from invenio_records_resources.services import SearchOptions as InvenioSearchOptions

from . import facets


class OaiRunSearchOptions(InvenioSearchOptions):
    """OaiRunRecord search options."""

    facet_groups = {}

    facets = {
        "harvester_name": facets.harvester_name,
        "manual": facets.manual,
        "status": facets.status,
        **getattr(InvenioSearchOptions, "facets", {}),
    }

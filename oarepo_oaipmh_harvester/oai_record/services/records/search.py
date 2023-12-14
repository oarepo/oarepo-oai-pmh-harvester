from oarepo_runtime.services.search import SearchOptions

from . import facets


class OaiRecordSearchOptions(SearchOptions):
    """OaiRecord search options."""

    facet_groups = {}

    facets = {
        "batch_id": facets.batch_id,
        "batch_started": facets.batch_started,
        "batch_sequence": facets.batch_sequence,
        "datestamp": facets.datestamp,
        "errors_code": facets.errors_code,
        "errors_location": facets.errors_location,
        "harvester_id": facets.harvester_id,
        "harvester_code": facets.harvester_code,
        "harvester_name": facets.harvester_name,
        "local_identifier": facets.local_identifier,
        "manual": facets.manual,
        "oai_identifier": facets.oai_identifier,
        "run_id": facets.run_id,
        "run_started": facets.run_started,
        **getattr(SearchOptions, "facets", {}),
    }

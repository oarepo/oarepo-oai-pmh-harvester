from invenio_records_resources.services import SearchOptions as InvenioSearchOptions
from flask_babelex import lazy_gettext as _

from . import facets


class OaiRecordSearchOptions(InvenioSearchOptions):
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
        **getattr(InvenioSearchOptions, "facets", {}),
    }

    # Translate sort option titles
    sort_options = {
        key: {k: _(v) if k == "title" else v for k, v in value.items()}
        for key, value in InvenioSearchOptions.sort_options.items()
    }

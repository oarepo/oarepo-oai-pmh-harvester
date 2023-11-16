from invenio_records_resources.services import SearchOptions as InvenioSearchOptions
from flask_babelex import lazy_gettext as _

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

    # Translate sort option titles
    sort_options = {
        key: {k: _(v) if k == "title" else v for k, v in value.items()}
        for key, value in InvenioSearchOptions.sort_options.items()
    }

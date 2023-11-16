from invenio_records_resources.services import SearchOptions as InvenioSearchOptions
from flask_babelex import lazy_gettext as _

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

    # Translate sort option titles
    sort_options = {
        key: {k: _(v) if k == "title" else v for k, v in value.items()}
        for key, value in InvenioSearchOptions.sort_options.items()
    }

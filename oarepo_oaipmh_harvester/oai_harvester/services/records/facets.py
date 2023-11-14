"""Facet definitions."""

from flask_babelex import lazy_gettext as _
from invenio_records_resources.services.records.facets import TermsFacet

batch_size = TermsFacet(field="batch_size", label=_("batch_size.label"))

loader = TermsFacet(field="loader", label=_("loader.label"))

max_records = TermsFacet(field="max_records", label=_("max_records.label"))

metadataprefix = TermsFacet(field="metadataprefix", label=_("metadataprefix.label"))

setspecs = TermsFacet(field="setspecs", label=_("setspecs.label"))

transformers = TermsFacet(field="transformers", label=_("transformers.label"))

"""Facet definitions."""

from flask_babelex import lazy_gettext as _
from invenio_records_resources.services.records.facets import TermsFacet
from oarepo_runtime.facets.date import DateTimeFacet

code = TermsFacet(field="code", label=_("code.label"))


baseurl = TermsFacet(field="baseurl", label=_("baseurl.label"))


metadataprefix = TermsFacet(field="metadataprefix", label=_("metadataprefix.label"))


name = TermsFacet(field="name", label=_("name.label"))


setspecs = TermsFacet(field="setspecs", label=_("setspecs.label"))


loader = TermsFacet(field="loader", label=_("loader.label"))


transformers = TermsFacet(field="transformers", label=_("transformers.label"))


writer = TermsFacet(field="writer", label=_("writer.label"))


max_records = TermsFacet(field="max_records", label=_("max_records.label"))


batch_size = TermsFacet(field="batch_size", label=_("batch_size.label"))


_id = TermsFacet(field="id", label=_("id.label"))


created = DateTimeFacet(field="created", label=_("created.label"))


updated = DateTimeFacet(field="updated", label=_("updated.label"))


_schema = TermsFacet(field="$schema", label=_("$schema.label"))

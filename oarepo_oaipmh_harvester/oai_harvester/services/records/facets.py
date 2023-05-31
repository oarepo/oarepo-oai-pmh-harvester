"""Facet definitions."""

from flask_babelex import lazy_gettext as _
from invenio_records_resources.services.records.facets import TermsFacet
from oarepo_runtime.facets.date import DateTimeFacet

_schema = TermsFacet(field="$schema", label=_("$schema.label"))

baseurl = TermsFacet(field="baseurl", label=_("baseurl.label"))

batch_size = TermsFacet(field="batch_size", label=_("batch_size.label"))

code = TermsFacet(field="code", label=_("code.label"))

created = DateTimeFacet(field="created", label=_("created.label"))

_id = TermsFacet(field="id", label=_("id.label"))

loader = TermsFacet(field="loader", label=_("loader.label"))

max_records = TermsFacet(field="max_records", label=_("max_records.label"))

metadataprefix = TermsFacet(field="metadataprefix", label=_("metadataprefix.label"))

name = TermsFacet(field="name", label=_("name.label"))

setspecs = TermsFacet(field="setspecs", label=_("setspecs.label"))

transformers = TermsFacet(field="transformers", label=_("transformers.label"))

updated = DateTimeFacet(field="updated", label=_("updated.label"))

writer = TermsFacet(field="writer", label=_("writer.label"))

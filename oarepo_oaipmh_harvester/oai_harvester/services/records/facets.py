"""Facet definitions."""

from invenio_records_resources.services.records.facets import TermsFacet
from invenio_search.engine import dsl
from oarepo_runtime.facets.nested_facet import NestedLabeledFacet

code = TermsFacet(field="code")


baseurl = TermsFacet(field="baseurl")


metadataprefix = TermsFacet(field="metadataprefix")


name = TermsFacet(field="name")


setspecs = TermsFacet(field="setspecs")


loader = TermsFacet(field="loader")


transformers = TermsFacet(field="transformers")


writer = TermsFacet(field="writer")


max_records = TermsFacet(field="max_records")


batch_size = TermsFacet(field="batch_size")


_id = TermsFacet(field="id")


created = TermsFacet(field="created")


updated = TermsFacet(field="updated")


_schema = TermsFacet(field="$schema")

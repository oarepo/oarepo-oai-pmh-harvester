"""Facet definitions."""

from invenio_records_resources.services.records.facets import TermsFacet
from invenio_search.engine import dsl
from oarepo_runtime.facets.nested_facet import NestedLabeledFacet

run_id = TermsFacet(field="run.id")


run__version = TermsFacet(field="run.@v")


status = TermsFacet(field="status")


identifiers = TermsFacet(field="identifiers")


errors_oai_identifier = TermsFacet(field="errors.oai_identifier")


errors_error_keyword = TermsFacet(field="errors.error.keyword")


started = TermsFacet(field="started")


finished = TermsFacet(field="finished")


_id = TermsFacet(field="id")


created = TermsFacet(field="created")


updated = TermsFacet(field="updated")


_schema = TermsFacet(field="$schema")

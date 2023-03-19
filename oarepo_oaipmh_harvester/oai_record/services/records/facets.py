"""Facet definitions."""

from invenio_records_resources.services.records.facets import TermsFacet
from invenio_search.engine import dsl
from oarepo_runtime.facets.nested_facet import NestedLabeledFacet

batch_id = TermsFacet(field="batch.id")


batch__version = TermsFacet(field="batch.@v")


local_identifier = TermsFacet(field="local_identifier")


oai_identifier = TermsFacet(field="oai_identifier")


datestamp = TermsFacet(field="datestamp")


status = TermsFacet(field="status")


warnings_keyword = TermsFacet(field="warnings.keyword")


errors_keyword = TermsFacet(field="errors.keyword")


_id = TermsFacet(field="id")


created = TermsFacet(field="created")


updated = TermsFacet(field="updated")


_schema = TermsFacet(field="$schema")

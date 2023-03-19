"""Facet definitions."""

from invenio_records_resources.services.records.facets import TermsFacet
from invenio_search.engine import dsl
from oarepo_runtime.facets.nested_facet import NestedLabeledFacet

harvester_id = TermsFacet(field="harvester.id")


harvester_code = TermsFacet(field="harvester.code")


harvester_baseurl = TermsFacet(field="harvester.baseurl")


harvester_metadataprefix = TermsFacet(field="harvester.metadataprefix")


harvester_name = TermsFacet(field="harvester.name")


harvester_setspecs = TermsFacet(field="harvester.setspecs")


harvester_loader = TermsFacet(field="harvester.loader")


harvester_transformers = TermsFacet(field="harvester.transformers")


harvester_writer = TermsFacet(field="harvester.writer")


harvester_max_records = TermsFacet(field="harvester.max_records")


harvester_batch_size = TermsFacet(field="harvester.batch_size")


harvester_created = TermsFacet(field="harvester.created")


harvester_updated = TermsFacet(field="harvester.updated")


harvester__schema = TermsFacet(field="harvester.$schema")


batches = TermsFacet(field="batches")


status = TermsFacet(field="status")


warning = TermsFacet(field="warning")


error = TermsFacet(field="error")


started = TermsFacet(field="started")


finished = TermsFacet(field="finished")


duration = TermsFacet(field="duration")


_id = TermsFacet(field="id")


created = TermsFacet(field="created")


updated = TermsFacet(field="updated")


_schema = TermsFacet(field="$schema")

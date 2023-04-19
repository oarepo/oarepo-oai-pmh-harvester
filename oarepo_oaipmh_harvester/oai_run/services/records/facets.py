"""Facet definitions."""

from flask_babelex import lazy_gettext as _
from invenio_records_resources.services.records.facets import TermsFacet
from oarepo_runtime.facets.date import DateTimeFacet
from oarepo_runtime.facets.enum import EnumTermsFacet

harvester_id = TermsFacet(field="harvester.id", label=_("harvester/id.label"))


harvester_code = TermsFacet(field="harvester.code", label=_("harvester/code.label"))


harvester_baseurl = TermsFacet(
    field="harvester.baseurl", label=_("harvester/baseurl.label")
)


harvester_metadataprefix = TermsFacet(
    field="harvester.metadataprefix", label=_("harvester/metadataprefix.label")
)


harvester_name = TermsFacet(field="harvester.name", label=_("harvester/name.label"))


harvester_setspecs = TermsFacet(
    field="harvester.setspecs", label=_("harvester/setspecs.label")
)


harvester_loader = TermsFacet(
    field="harvester.loader", label=_("harvester/loader.label")
)


harvester_transformers = TermsFacet(
    field="harvester.transformers", label=_("harvester/transformers.label")
)


harvester_writer = TermsFacet(
    field="harvester.writer", label=_("harvester/writer.label")
)


harvester_max_records = TermsFacet(
    field="harvester.max_records", label=_("harvester/max_records.label")
)


harvester_batch_size = TermsFacet(
    field="harvester.batch_size", label=_("harvester/batch_size.label")
)


harvester_created = DateTimeFacet(
    field="harvester.created", label=_("harvester/created.label")
)


harvester_updated = DateTimeFacet(
    field="harvester.updated", label=_("harvester/updated.label")
)


harvester__schema = TermsFacet(
    field="harvester.$schema", label=_("harvester/$schema.label")
)


batches = TermsFacet(field="batches", label=_("batches.label"))


status = EnumTermsFacet(field="status", label=_("status.label"))


warning = TermsFacet(field="warning", label=_("warning.label"))


error = TermsFacet(field="error", label=_("error.label"))


started = DateTimeFacet(field="started", label=_("started.label"))


finished = DateTimeFacet(field="finished", label=_("finished.label"))


duration = TermsFacet(field="duration", label=_("duration.label"))


_id = TermsFacet(field="id", label=_("id.label"))


created = DateTimeFacet(field="created", label=_("created.label"))


updated = DateTimeFacet(field="updated", label=_("updated.label"))


_schema = TermsFacet(field="$schema", label=_("$schema.label"))

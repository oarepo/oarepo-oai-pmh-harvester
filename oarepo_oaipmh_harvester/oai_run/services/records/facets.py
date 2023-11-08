"""Facet definitions."""

from flask_babelex import lazy_gettext as _
from invenio_records_resources.services.records.facets import TermsFacet
from oarepo_runtime.facets.date import DateTimeFacet

_schema = TermsFacet(field="$schema", label=_("$schema.label"))

created = DateTimeFacet(field="created", label=_("created.label"))

created_batches = TermsFacet(field="created_batches", label=_("created_batches.label"))

duration = TermsFacet(field="duration", label=_("duration.label"))

errors = TermsFacet(field="errors", label=_("errors.label"))

finished = DateTimeFacet(field="finished", label=_("finished.label"))

finished_batches = TermsFacet(
    field="finished_batches", label=_("finished_batches.label")
)

harvester_id = TermsFacet(field="harvester.id", label=_("harvester/id.label"))

harvester_code = TermsFacet(field="harvester.code", label=_("harvester/code.label"))

harvester__version = TermsFacet(field="harvester.@v", label=_("harvester/@v.label"))

_id = TermsFacet(field="id", label=_("id.label"))

manual = TermsFacet(field="manual", label=_("manual.label"))

started = DateTimeFacet(field="started", label=_("started.label"))

status = TermsFacet(field="status", label=_("status.label"))

title = TermsFacet(field="title.keyword", label=_("title.label"))

total_batches = TermsFacet(field="total_batches", label=_("total_batches.label"))

updated = DateTimeFacet(field="updated", label=_("updated.label"))

warnings = TermsFacet(field="warnings", label=_("warnings.label"))

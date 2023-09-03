"""Facet definitions."""

from flask_babelex import lazy_gettext as _
from invenio_records_resources.services.records.facets import TermsFacet
from oarepo_runtime.facets.date import DateTimeFacet

_schema = TermsFacet(field="$schema", label=_("$schema.label"))

batches = TermsFacet(field="batches", label=_("batches.label"))

created = DateTimeFacet(field="created", label=_("created.label"))

duration = TermsFacet(field="duration", label=_("duration.label"))

error = TermsFacet(field="error", label=_("error.label"))

finished = DateTimeFacet(field="finished", label=_("finished.label"))

harvester_id = TermsFacet(field="harvester.id", label=_("harvester/id.label"))

harvester_code = TermsFacet(field="harvester.code", label=_("harvester/code.label"))

harvester__version = TermsFacet(field="harvester.@v", label=_("harvester/@v.label"))

_id = TermsFacet(field="id", label=_("id.label"))

manual = TermsFacet(field="manual", label=_("manual.label"))

started = DateTimeFacet(field="started", label=_("started.label"))

status = TermsFacet(field="status", label=_("status.label"))

updated = DateTimeFacet(field="updated", label=_("updated.label"))

warning = TermsFacet(field="warning", label=_("warning.label"))

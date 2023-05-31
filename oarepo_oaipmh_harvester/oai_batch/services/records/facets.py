"""Facet definitions."""

from flask_babelex import lazy_gettext as _
from invenio_records_resources.services.records.facets import TermsFacet
from oarepo_runtime.facets.date import DateTimeFacet

_schema = TermsFacet(field="$schema", label=_("$schema.label"))

created = DateTimeFacet(field="created", label=_("created.label"))

errors_error_message = TermsFacet(
    field="errors.error_message.keyword", label=_("errors/error_message.label")
)

errors_error_type = TermsFacet(
    field="errors.error_type", label=_("errors/error_type.label")
)

errors_oai_identifier = TermsFacet(
    field="errors.oai_identifier", label=_("errors/oai_identifier.label")
)

finished = DateTimeFacet(field="finished", label=_("finished.label"))

_id = TermsFacet(field="id", label=_("id.label"))

identifiers = TermsFacet(field="identifiers", label=_("identifiers.label"))

manual = TermsFacet(field="manual", label=_("manual.label"))

run_id = TermsFacet(field="run.id", label=_("run/id.label"))

run__version = TermsFacet(field="run.@v", label=_("run/@v.label"))

started = DateTimeFacet(field="started", label=_("started.label"))

status = TermsFacet(field="status", label=_("status.label"))

updated = DateTimeFacet(field="updated", label=_("updated.label"))

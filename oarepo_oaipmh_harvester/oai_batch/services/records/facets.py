"""Facet definitions."""

from flask_babelex import lazy_gettext as _
from invenio_records_resources.services.records.facets import TermsFacet
from oarepo_runtime.facets.date import DateTimeFacet
from oarepo_runtime.facets.enum import EnumTermsFacet

run_id = TermsFacet(field="run.id", label=_("run/id.label"))


run__version = TermsFacet(field="run.@v", label=_("run/@v.label"))


status = EnumTermsFacet(field="status", label=_("status.label"))


identifiers = TermsFacet(field="identifiers", label=_("identifiers.label"))


errors_oai_identifier = TermsFacet(
    field="errors.oai_identifier", label=_("errors/oai_identifier.label")
)


errors_error_keyword = TermsFacet(
    field="errors.error.keyword", label=_("errors/error/keyword.label")
)


started = DateTimeFacet(field="started", label=_("started.label"))


finished = DateTimeFacet(field="finished", label=_("finished.label"))


_id = TermsFacet(field="id", label=_("id.label"))


created = DateTimeFacet(field="created", label=_("created.label"))


updated = DateTimeFacet(field="updated", label=_("updated.label"))


_schema = TermsFacet(field="$schema", label=_("$schema.label"))

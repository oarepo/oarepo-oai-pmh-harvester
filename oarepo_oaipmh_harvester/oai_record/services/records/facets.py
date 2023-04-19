"""Facet definitions."""

from flask_babelex import lazy_gettext as _
from invenio_records_resources.services.records.facets import TermsFacet
from oarepo_runtime.facets.date import DateTimeFacet
from oarepo_runtime.facets.enum import EnumTermsFacet

batch_id = TermsFacet(field="batch.id", label=_("batch/id.label"))


batch__version = TermsFacet(field="batch.@v", label=_("batch/@v.label"))


local_identifier = TermsFacet(
    field="local_identifier", label=_("local_identifier.label")
)


oai_identifier = TermsFacet(field="oai_identifier", label=_("oai_identifier.label"))


datestamp = DateTimeFacet(field="datestamp", label=_("datestamp.label"))


status = EnumTermsFacet(field="status", label=_("status.label"))


warnings_keyword = TermsFacet(
    field="warnings.keyword", label=_("warnings/keyword.label")
)


errors_keyword = TermsFacet(field="errors.keyword", label=_("errors/keyword.label"))


_id = TermsFacet(field="id", label=_("id.label"))


created = DateTimeFacet(field="created", label=_("created.label"))


updated = DateTimeFacet(field="updated", label=_("updated.label"))


_schema = TermsFacet(field="$schema", label=_("$schema.label"))

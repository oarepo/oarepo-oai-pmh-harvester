"""Facet definitions."""

from invenio_records_resources.services.records.facets import TermsFacet
from oarepo_runtime.i18n import lazy_gettext as _

harvester_name = TermsFacet(field="harvester.name", label=_("harvester/name.label"))

manual = TermsFacet(field="manual", label=_("manual.label"))

records_errors_code = TermsFacet(
    field="records.errors.code", label=_("records/errors/code.label")
)

status = TermsFacet(field="status", label=_("status.label"))

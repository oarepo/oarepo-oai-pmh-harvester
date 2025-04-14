from invenio_i18n import lazy_gettext as _
from invenio_records_resources.services.records.facets.facets import TermsFacet

harvester = TermsFacet(field="harvester_id", label=_("Harvester ID"))
deleted = TermsFacet(
    field="deleted",
    label=_("Deleted"),
    value_labels={True: _("Yes"), False: _("No")},
)

has_errors = TermsFacet(
    field="has_errors",
    label=_("Errors"),
    value_labels={True: _("Yes"), False: _("No")},
)
has_warnings = TermsFacet(
    field="has_warnings",
    label=_("Warnings"),
    value_labels={True: _("Yes"), False: _("No")},
)

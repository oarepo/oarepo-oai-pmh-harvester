from invenio_i18n import lazy_gettext as _
from invenio_records_resources.services.records.facets.facets import TermsFacet

harvester = TermsFacet(field="harvester_id", label=_("Harvester ID"))
harvester_name = TermsFacet(field="harvester_name", label=_("Harvester name"))
manual = TermsFacet(
    field="manual",
    label=_("Manual run"),
)
status = TermsFacet(
    field="status",
    label=_("Status"),
    value_labels={
        "running": _("Harvest running"),
        "finishing": _("Harvest finishing"),
        "finished": _("Harvest finished"),
        "failed": _("Harvest failed"),
        "stopped": _("Harvest stopped"),
        "cancelled": _("Harvest cancelled"),
    },
)

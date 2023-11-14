"""Facet definitions."""

from flask_babelex import lazy_gettext as _
from invenio_records_resources.services.records.facets import TermsFacet

harvester_name = TermsFacet(field="harvester.name", label=_("harvester/name.label"))

manual = TermsFacet(field="manual", label=_("manual.label"))

status = TermsFacet(field="status", label=_("status.label"))

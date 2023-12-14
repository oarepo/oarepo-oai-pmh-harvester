"""Facet definitions."""

from invenio_records_resources.services.records.facets import TermsFacet
from oarepo_runtime.i18n import lazy_gettext as _
from oarepo_runtime.services.facets.date import DateTimeFacet

batch_id = TermsFacet(field="batch.id", label=_("batch/id.label"))

batch_started = DateTimeFacet(field="batch.started", label=_("batch/started.label"))

batch_sequence = TermsFacet(field="batch.sequence", label=_("batch/sequence.label"))

datestamp = DateTimeFacet(field="datestamp", label=_("datestamp.label"))

errors_code = TermsFacet(field="errors.code", label=_("errors/code.label"))

errors_location = TermsFacet(field="errors.location", label=_("errors/location.label"))

harvester_id = TermsFacet(field="harvester.id", label=_("harvester/id.label"))

harvester_code = TermsFacet(field="harvester.code", label=_("harvester/code.label"))

harvester_name = TermsFacet(field="harvester.name", label=_("harvester/name.label"))

local_identifier = TermsFacet(
    field="local_identifier", label=_("local_identifier.label")
)

manual = TermsFacet(field="manual", label=_("manual.label"))

oai_identifier = TermsFacet(field="oai_identifier", label=_("oai_identifier.label"))

run_id = TermsFacet(field="run.id", label=_("run/id.label"))

run_started = DateTimeFacet(field="run.started", label=_("run/started.label"))

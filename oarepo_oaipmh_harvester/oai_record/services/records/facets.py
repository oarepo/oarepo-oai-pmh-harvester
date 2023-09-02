"""Facet definitions."""

from flask_babelex import lazy_gettext as _
from invenio_records_resources.services.records.facets import TermsFacet
from oarepo_runtime.facets.date import DateTimeFacet

_schema = TermsFacet(field="$schema", label=_("$schema.label"))

batch_id = TermsFacet(field="batch.id", label=_("batch/id.label"))

batch__version = TermsFacet(field="batch.@v", label=_("batch/@v.label"))

created = DateTimeFacet(field="created", label=_("created.label"))

datestamp = DateTimeFacet(field="datestamp", label=_("datestamp.label"))

errors_code = TermsFacet(field="errors.code", label=_("errors/code.label"))

errors_location = TermsFacet(field="errors.location", label=_("errors/location.label"))

errors_message = TermsFacet(
    field="errors.message.keyword", label=_("errors/message.label")
)

harvester_id = TermsFacet(field="harvester.id", label=_("harvester/id.label"))

harvester__version = TermsFacet(field="harvester.@v", label=_("harvester/@v.label"))

_id = TermsFacet(field="id", label=_("id.label"))

local_identifier = TermsFacet(
    field="local_identifier", label=_("local_identifier.label")
)

manual = TermsFacet(field="manual", label=_("manual.label"))

oai_identifier = TermsFacet(field="oai_identifier", label=_("oai_identifier.label"))

status = TermsFacet(field="status", label=_("status.label"))

updated = DateTimeFacet(field="updated", label=_("updated.label"))

warnings = TermsFacet(field="warnings.keyword", label=_("warnings.label"))

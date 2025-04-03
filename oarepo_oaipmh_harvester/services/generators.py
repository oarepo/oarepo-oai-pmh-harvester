#
# Copyright (C) 2025 CESNET z.s.p.o.
#
# oarepo-workflows is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.
#
"""Permission generators for OAI-harvested records."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from invenio_records_permissions.generators import ConditionalGenerator, Generator
from invenio_search.engine import dsl

if TYPE_CHECKING:
    from invenio_records_resources.records import Record


class IfHarvested(ConditionalGenerator):
    """Generator that checks if the record has been harvested.

    Example:
        .. code-block:: python

            can_edit = [ IfHarvested(Disable(), [RecordOwners()]) ]
    """

    def __init__(
        self,
        then_: list[Generator] | tuple[Generator] | Generator | None = None,
        else_: list[Generator] | tuple[Generator] | Generator | None = None,
    ) -> None:
        """Initialize the generator."""
        if isinstance(then_, Generator):
            then_ = [then_]
        if isinstance(else_, Generator):
            else_ = [else_]
        super().__init__(then_ or [], else_=else_ or [])

    def _condition(self, record: Record, **context: Any) -> bool:
        """Check if the record is in the state."""
        oai_section = record.get("oai", None)
        if not oai_section:
            return False
        harvest = oai_section.get("harvest", None)
        if not harvest:
            return False
        identifier = harvest.get("identifier")
        return bool(identifier)

    def query_filter(self, **context: Any) -> dsl.Q:
        """Apply then or else filter."""
        field = "state"

        q_harvested = dsl.Q("exists", field="oai.harvest.identifier")
        if self.then_:
            then_query = self._make_query(self.then_, **context)
        else:
            then_query = dsl.Q("match_none")

        if self.else_:
            else_query = self._make_query(self.else_, **context)
        else:
            else_query = dsl.Q("match_none")

        return (q_harvested & then_query) | (~q_harvested & else_query)

    def __repr__(self) -> str:
        """Representation of the generator."""
        return f"IfHarvested({self.state}, then={repr(self.then_)}, else={repr(self.else_)})"

    def __str__(self) -> str:
        """String representation of the generator."""
        return repr(self)


class IfNotHarvested(IfHarvested):
    def _condition(self, record: Record, **context: Any) -> bool:
        return not super()._condition(record, **context)

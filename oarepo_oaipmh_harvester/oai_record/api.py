from datetime import datetime

from invenio_db import db
from invenio_records.dumpers import SearchDumper
from invenio_records.dumpers.indexedat import IndexedAtDumperExt
from invenio_records.systemfields import ModelField
from invenio_records_resources.records.systemfields import IndexField
from invenio_users_resources.records.api import BaseAggregate

from ..models import OAIHarvestedRecord
from .dumpers import AddHarvesterDumperExt
from .models import OAIRecordAggregateModel


class OAIRecordAggregate(BaseAggregate):
    """An aggregate of information about a user."""

    model_cls = OAIRecordAggregateModel
    """The model class for the request."""

    dumper = SearchDumper(
        extensions=[
            IndexedAtDumperExt(),
            AddHarvesterDumperExt(),
        ],
        model_fields={
            "id": ("uuid", str),
        },
    )
    """Search dumper with configured extensions."""

    index = IndexField(
        "oai-harvest-record-oai-harvest-record-v1.0.0",
        search_alias="oai-harvest-record",
    )
    """The search engine index to use."""

    oai_identifier = ModelField("oai_identifier", dump_type=str)
    """The OAI identifier of the record."""
    record_id = ModelField("record_id", dump_type=str)
    """The record ID of the record."""
    datestamp = ModelField("datestamp", dump_type=datetime)
    """The datestamp of the record."""
    harvested_at = ModelField("harvested_at", dump_type=datetime)
    """The time when the record was harvested."""
    deleted = ModelField("deleted", dump_type=bool)
    """True if the record was deleted during the harvest."""
    has_errors = ModelField("has_errors", dump_type=bool)
    """True if the record has errors during the harvest."""
    has_warnings = ModelField("has_warnings", dump_type=bool)
    """True if the record has warnings during the harvest."""
    errors = ModelField("errors", dump_type=list[dict])
    """Errors."""
    original_data = ModelField("original_data", dump_type=dict)
    """Original data."""
    transformed_data = ModelField("transformed_data", dump_type=dict)
    """Transformed data."""
    run_id = ModelField("run_id", dump_type=str)
    """The run ID of the record."""

    @classmethod
    def create(cls, data, id_=None, validator=None, format_checker=None, **kwargs):
        """Create a new User and store it in the database."""
        with db.session.begin_nested():
            record = OAIHarvestedRecord(**data)
            db.session.add(record)
            return cls.from_model(record)

    @classmethod
    def get_record(cls, id_):
        """Get the user via the specified ID."""
        with db.session.no_autoflush:
            record = OAIHarvestedRecord.query.get(id_)
            return cls.from_model(record)


def oai_harvest_record_generator(model_class):
    import sys

    import click

    from oarepo_oaipmh_harvester.oai_record.models import OAIHarvestedRecord

    try:
        for x in db.session.query(OAIHarvestedRecord.oai_identifier):
            rec_id = x[0]
            yield OAIRecordAggregate.get_record(rec_id)
    except Exception as e:
        click.secho(f"Could not index {model_class}: {e}", fg="red", file=sys.stderr)

from datetime import datetime
from uuid import UUID

from invenio_db import db
from invenio_records.dumpers import SearchDumper
from invenio_records.dumpers.indexedat import IndexedAtDumperExt
from invenio_records.systemfields import ModelField
from invenio_records_resources.records.systemfields import IndexField
from invenio_users_resources.records.api import BaseAggregate

from ..models import OAIHarvesterRun
from .dumpers import AddHarvesterDumperExt
from .models import OAIRunAggregateModel


class OAIRunAggregate(BaseAggregate):
    """An aggregate of information about a user."""

    model_cls = OAIRunAggregateModel
    """The model class for the request."""

    # NOTE: the "uuid" isn't a UUID but contains the same value as the "id"
    #       field, which is currently an integer for User objects!
    dumper = SearchDumper(
        extensions=[IndexedAtDumperExt(), AddHarvesterDumperExt()],
        model_fields={
            "id": ("uuid", UUID),
        },
    )
    """Search dumper with configured extensions."""

    index = IndexField(
        "oai-harvest-run-oai-harvest-run-v1.0.0", search_alias="oai-harvest-run"
    )
    """The search engine index to use."""

    id = ModelField("id", dump_type=UUID)
    """The user identifier."""

    harvester_id = ModelField("harvester_id", dump_type=str)
    """The harvester identifier."""

    manual = ModelField("manual", dump_type=bool)
    """True if the run was started manually."""

    title = ModelField("title", dump_type=str)
    """The title of the run."""

    harvester_config = ModelField("harvester_config", dump_type=dict)
    """The harvester configuration used for the run."""

    start_time = ModelField("start_time", dump_type=datetime)
    """The time when the run started."""

    end_time = ModelField("end_time", dump_type=datetime)
    """The time when the run ended."""

    last_update_time = ModelField("last_update_time", dump_type=datetime)
    """The time when the run was last updated."""

    status = ModelField("status", dump_type=str)
    """The status of the run."""

    records = ModelField("records", dump_type=int)
    """The number of records processed during the run."""

    finished_records = ModelField("finished_records", dump_type=int)
    """The number of records that were finished during the run."""

    ok_records = ModelField("ok_records", dump_type=int)
    """The number of records that were successfully processed."""

    failed_records = ModelField("failed_records", dump_type=int)
    """The number of records that failed during processing."""

    @classmethod
    def create(cls, data, id_=None, validator=None, format_checker=None, **kwargs):
        """Create a new User and store it in the database."""
        with db.session.begin_nested():
            run = OAIHarvesterRun(**data)
            db.session.add(run)
            return cls.from_model(run)

    @classmethod
    def get_record(cls, id_):
        """Get the user via the specified ID."""
        with db.session.no_autoflush:
            run = OAIHarvesterRun.query.get(id_)
            return cls.from_model(run)


def oai_harvest_run_generator(model_class):
    import sys

    import click

    from oarepo_oaipmh_harvester.oai_run.models import OAIHarvesterRun

    try:
        for x in db.session.query(OAIHarvesterRun.id):
            rec_id = x[0]
            yield OAIRunAggregate.get_record(rec_id)
    except Exception as e:
        click.secho(f"Could not index {model_class}: {e}", fg="red", file=sys.stderr)

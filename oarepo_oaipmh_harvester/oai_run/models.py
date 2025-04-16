from invenio_db import db
from invenio_users_resources.records.models import AggregateMetadata

from oarepo_oaipmh_harvester.models import OAIHarvesterRun


class OAIRunAggregateModel(AggregateMetadata):
    """OAI Run aggregate data model."""

    # If you add properties here you likely also want to add a ModelField on
    # the UserAggregate API class.
    _properties = [
        "id",
        "harvester_id",
        "manual",
        "title",
        "harvester_config",
        "start_time",
        "end_time",
        "last_update_time",
        "status",
        "records",
        "finished_records",
        "ok_records",
        "failed_records",
    ]
    """Properties of this object that can be accessed."""

    _set_properties = []
    """Properties of this object that can be set."""

    @property
    def model_obj(self):
        """The actual model object behind this user aggregate."""
        if self._model_obj is None:
            id_ = self._data.get("id")
            with db.session.no_autoflush:
                self._model_obj = OAIHarvesterRun.query.get(id_)
        return self._model_obj

    @property
    def version_id(self):
        """Return the version ID of the record."""
        return 1

    @property
    def created(self):
        """Return the creation date of the record."""
        return self.start_time

    @property
    def updated(self):
        """Return the last update date of the record."""
        return self.last_update_time or self.start_time

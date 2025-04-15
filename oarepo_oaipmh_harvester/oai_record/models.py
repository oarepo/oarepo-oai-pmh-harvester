from invenio_db import db
from invenio_users_resources.records.models import AggregateMetadata

from oarepo_oaipmh_harvester.models import OAIHarvestedRecord


class OAIRecordAggregateModel(AggregateMetadata):
    """OAI Run aggregate data model."""

    # If you add properties here you likely also want to add a ModelField on
    # the UserAggregate API class.
    _properties = [
        "oai_identifier",
        "record_id",
        "datestamp",
        "harvested_at",
        "deleted",
        "has_errors",
        "has_warnings",
        "errors",
        "original_data",
        "transformed_data",
        "run_id",
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
                self._model_obj = OAIHarvestedRecord.query.get(id_)
        return self._model_obj

    @property
    def version_id(self):
        """Return the version ID of the record."""
        return 1

    @property
    def created(self):
        """Return the creation date of the record."""
        return self.datestamp

    @property
    def updated(self):
        """Return the last update date of the record."""
        return self.datestamp

    @property
    def id(self):
        """Return the ID of the record."""
        return self.oai_identifier

from invenio_access.permissions import system_identity
from invenio_records.dumpers.search import SearchDumperExt

from oarepo_oaipmh_harvester.oai_harvester.proxies import (
    current_service as oai_harvester_service,
)


class AddHarvesterDumperExt(SearchDumperExt):
    """Base class for OAI record dumpers."""

    def dump(self, record, data):
        """Dump the data."""

        harvester = oai_harvester_service.read(system_identity, id_=record.harvester_id)
        data["harvester_name"] = harvester.data["name"]
        data["harvest_managers"] = [
            x["id"] for x in harvester._record.get("harvest_managers", [])
        ]
        return data

    def load(self, data, record_cls):
        """Load the data.

        Reverse the changes made by the dump method.
        """
        data.pop("harvest_managers", None)
        data.pop("harvester_name", None)
        return data

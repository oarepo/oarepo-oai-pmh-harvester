from typing import Any, Dict, List

from invenio_records_resources.proxies import current_service_registry
from oarepo_runtime.datastreams import StreamBatch, StreamEntry
from oarepo_runtime.datastreams.transformers import BaseTransformer

from oarepo_oaipmh_harvester.oai_record.proxies import (
    current_service as oai_record_service,
)


def dict_lookup_ignore_arrays(source: Any, lookup_key: List[str]):
    if not lookup_key:
        yield source
    else:
        if isinstance(source, list):
            for item in source:
                yield from dict_lookup_ignore_arrays(item, lookup_key)
        elif isinstance(source, dict) and lookup_key[0] in source:
            yield from dict_lookup_ignore_arrays(source[lookup_key[0]], lookup_key[1:])


class OAIRecordLookupTransformer(BaseTransformer):
    """
    Looks up target records and oai records for the given batch and filters out
    the records that have the same datestamp and have been harvested successfully
    during the previous harvest.

    If there was a previous harvest error, the oai record id is stored in the
    batch entry context so that it can be deleted later in oai writer
    """

    def __init__(
        self,
        identity=None,
        oai_identifier_field="oai.harvest.identifier",
        oai_datestamp_field="oai.harvest.datestamp",
        oai_identifier_facet=None,
        oai_datestamp_facet=None,
        harvested_record_service=None,
        overwrite_all_records=False,
        **kwargs,
    ):
        super().__init__()
        assert identity is not None, "Identity must be set"
        assert (
            harvested_record_service is not None
        ), "Harvested record service must be set for record lookup transformer"
        self._identity = identity
        self._oai_identifier_field = oai_identifier_field.split(".")
        self._oai_datestamp_field = oai_datestamp_field.split(".")
        self._oai_identifier_facet = (
            oai_identifier_facet or oai_identifier_field.replace(".", "_")
        )
        self._oai_datestamp_facet = oai_datestamp_facet or oai_datestamp_field.replace(
            ".", "_"
        )
        self._harvested_record_service = current_service_registry.get(
            harvested_record_service
        )
        self._overwrite_all_records = overwrite_all_records

    def apply(self, batch: StreamBatch, *args, **kwargs) -> StreamBatch:
        by_oai_identifier = {
            entry.context["oai"]["identifier"]: entry for entry in batch.entries
        }
        if not by_oai_identifier:
            return batch

        self.copy_harvest_metadata_to_entries(batch)
        self.filter_successfully_harvested_records(by_oai_identifier)
        self.mark_previously_failed_records(by_oai_identifier)

        return batch

    def copy_harvest_metadata_to_entries(self, batch):
        for entry in batch.entries:
            harvest_metadata = entry.entry.setdefault("oai", {}).setdefault(
                "harvest", {}
            )
            harvest_metadata["datestamp"] = entry.context["oai"]["datestamp"]
            harvest_metadata["identifier"] = entry.context["oai"]["identifier"]

    def mark_previously_failed_records(self, by_oai_identifier: Dict[str, StreamEntry]):
        # the oai records are those that have had errors during the previous harvest
        oai_records = list(
            oai_record_service.scan(
                self._identity,
                params={"facets": {"oai_identifier": list(by_oai_identifier.keys())}},
            )
        )
        for oai_record in oai_records:
            entry = by_oai_identifier[oai_record["oai_identifier"]]
            # just tie the oai record id to the batch entry so that if it was harvested
            # successfully during the previous harvest, we can delete it
            entry.context["oai"]["oai_record_id"] = oai_record["id"]

    def filter_successfully_harvested_records(
        self, by_oai_identifier: Dict[str, StreamEntry]
    ):
        """
        Filters out the records that have been harvested successfully during the previous harvest
        if they have not been modified since then.

        :param by_oai_identifier: the batch entries indexed by oai identifier
        """
        # these are the records that have been harvested successfully during the previous harvest
        harvested_records = list(
            self._harvested_record_service.scan(
                self._identity,
                params={
                    "facets": {
                        self._oai_identifier_facet: list(by_oai_identifier.keys())
                    }
                },
                fields=["id", self._oai_identifier_field, self._oai_datestamp_field],
            )
        )

        for harvested_record in harvested_records:
            # TODO: handle multiple harvested sources for a single record
            try:
                oai_identifier = list(
                    dict_lookup_ignore_arrays(
                        harvested_record, self._oai_identifier_field
                    )
                )[0]
            except:
                raise KeyError(
                    f"Could not get {self._oai_identifier_field} in {harvested_record}."
                    f"This should never happen, please make sure that the oai record"
                    f"lookup has the correct configuration of oai_identifier_field,"
                    f" oai_datestamp_field, oai_identifier_facet and oai_datestamp_facet."
                )
            entry = by_oai_identifier[oai_identifier]
            entry.entry["id"] = harvested_record["id"]
            entry.id = harvested_record["id"]
            datestamp = list(
                dict_lookup_ignore_arrays(harvested_record, self._oai_datestamp_field)
            )[0]

            if not self._overwrite_all_records and datestamp == entry.context["oai"]["datestamp"]:
                # do not save the item as it has the same datestamp
                entry.filtered = True

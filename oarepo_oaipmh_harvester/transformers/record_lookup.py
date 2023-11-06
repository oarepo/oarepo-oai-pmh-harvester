from oarepo_runtime.datastreams import StreamBatch
from oarepo_runtime.datastreams.transformers import BaseTransformer

from oarepo_oaipmh_harvester.oai_record.proxies import current_service as record_service


class OAIRecordLookupTransformer(BaseTransformer):
    """
    Looks up oai records for the given batch and filters out the records that have the same datestamp.
    It also stores the oai record id into the batch entry context so that it can be used in oairecord writer
    to decide whether to create a new oai record or update an existing one.
    """

    def __init__(self, identity=None, **kwargs):
        super().__init__()
        assert identity is not None
        self._identity = identity

    def apply(self, batch: StreamBatch, *args, **kwargs) -> StreamBatch:
        by_oai_identifier = {
            entry.context["oai"]["identifier"]: entry for entry in batch.entries
        }

        for oai_record in list(
            record_service.scan(
                self._identity,
                params={"facets": {"oai_identifier": list(by_oai_identifier.keys())}},
            )
        ):
            entry = by_oai_identifier[oai_record["oai_identifier"]]
            entry.context["oai"]["oai_record_id"] = oai_record["id"]

            if oai_record and oai_record.get("local_identifier"):
                entry.entry["id"] = oai_record["local_identifier"]
                entry.id = oai_record["local_identifier"]
                if (
                    oai_record["status"] == "O"
                    and oai_record["datestamp"] == entry.context["oai"]["datestamp"]
                ):
                    # do not save the item as it has the same datestamp
                    entry.filtered = True

        return batch

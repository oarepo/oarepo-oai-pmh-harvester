import datetime

from invenio_access.permissions import system_identity
from oarepo_runtime.datastreams import StreamBatch
from oarepo_runtime.datastreams.transformers import BaseTransformer

from oarepo_oaipmh_harvester.oai_batch.proxies import current_service as batch_service


class OAIBatchTransformer(BaseTransformer):
    def __init__(self, *, identity, oai_run, manual, **kwargs) -> None:
        super().__init__()
        self.identity = identity
        self.oai_run = oai_run
        self.manual = manual

    def apply(self, batch: StreamBatch, *args, **kwargs) -> StreamBatch:
        batch_el = batch_service.create(
            system_identity,
            {
                "run": {"id": self.oai_run},
                "status": "R",
                "identifiers": [x.context["oai"]["identifier"] for x in batch.entries],
                "started": datetime.datetime.utcnow().isoformat() + "+00:00",
                "manual": self.manual,
            },
        )
        batch.context["batch_id"] = batch_el["id"]
        for e in batch.entries:
            e.context["oai_batch"] = batch_el["id"]
            e.context["manual"] = self.manual
        return batch

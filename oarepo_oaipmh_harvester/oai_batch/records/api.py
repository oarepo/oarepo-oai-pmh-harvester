from invenio_pidstore.providers.recordid_v2 import RecordIdProviderV2
from invenio_records.systemfields import ConstantField
from invenio_records_resources.records.api import Record as InvenioRecord
from invenio_records_resources.records.systemfields import IndexField
from invenio_records_resources.records.systemfields.pid import PIDField, PIDFieldContext
from oarepo_runtime.records.relations import PIDRelation, RelationsField

from oarepo_oaipmh_harvester.oai_batch.records.dumpers.dumper import OaiBatchDumper
from oarepo_oaipmh_harvester.oai_batch.records.models import OaiBatchMetadata
from oarepo_oaipmh_harvester.oai_harvester.records.api import OaiHarvesterRecord
from oarepo_oaipmh_harvester.oai_run.records.api import OaiRunRecord


class OaiBatchIdProvider(RecordIdProviderV2):
    pid_type = "btch"


class OaiBatchRecord(InvenioRecord):

    model_cls = OaiBatchMetadata

    schema = ConstantField("$schema", "local://oai_batch-1.0.0.json")

    index = IndexField(
        "oarepo-oaipmh-batch-oai_batch-1.0.0",
    )

    pid = PIDField(
        provider=OaiBatchIdProvider, context_cls=PIDFieldContext, create=True
    )

    dumper = OaiBatchDumper()

    relations = RelationsField(
        harvester=PIDRelation(
            "harvester",
            keys=["id", "code", "name"],
            pid_field=OaiHarvesterRecord.pid,
        ),
        run=PIDRelation(
            "run",
            keys=["id", "title", "started"],
            pid_field=OaiRunRecord.pid,
        ),
    )

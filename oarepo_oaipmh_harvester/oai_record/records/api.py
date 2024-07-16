from invenio_pidstore.providers.recordid_v2 import RecordIdProviderV2
from invenio_records.systemfields import ConstantField
from invenio_records_resources.records.api import Record as InvenioRecord
from invenio_records_resources.records.systemfields import IndexField
from invenio_records_resources.records.systemfields.pid import PIDField, PIDFieldContext
from oarepo_runtime.records.relations import PIDRelation, RelationsField

from oarepo_oaipmh_harvester.oai_batch.records.api import OaiBatchRecord
from oarepo_oaipmh_harvester.oai_harvester.records.api import OaiHarvesterRecord
from oarepo_oaipmh_harvester.oai_record.records.dumpers.dumper import OaiRecordDumper
from oarepo_oaipmh_harvester.oai_record.records.models import OaiRecordMetadata
from oarepo_oaipmh_harvester.oai_run.records.api import OaiRunRecord


class OaiRecordIdProvider(RecordIdProviderV2):
    pid_type = "rcrd"


class OaiRecord(InvenioRecord):

    model_cls = OaiRecordMetadata

    schema = ConstantField("$schema", "local://oai_record-1.0.0.json")

    index = IndexField(
        "oarepo-oaipmh-record-oai_record-1.0.0",
    )

    pid = PIDField(
        provider=OaiRecordIdProvider, context_cls=PIDFieldContext, create=True
    )

    dumper = OaiRecordDumper()

    relations = RelationsField(
        batch=PIDRelation(
            "batch",
            keys=["id", "started", "sequence"],
            pid_field=OaiBatchRecord.pid,
        ),
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

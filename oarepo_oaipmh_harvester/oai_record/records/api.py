from invenio_pidstore.providers.recordid_v2 import RecordIdProviderV2
from invenio_records.systemfields import ConstantField, RelationsField
from invenio_records_resources.records.api import Record
from invenio_records_resources.records.systemfields import IndexField
from invenio_records_resources.records.systemfields.pid import PIDField, PIDFieldContext
from oarepo_runtime.relations import PIDRelation, RelationsField

from oarepo_oaipmh_harvester.oai_batch.records.api import OaiBatchRecord
from oarepo_oaipmh_harvester.oai_record.records.dumper import OaiRecordDumper
from oarepo_oaipmh_harvester.oai_record.records.models import OaiRecordMetadata


class OaiRecordIdProvider(RecordIdProviderV2):
    pid_type = "_rcrd"


class OaiRecordRecord(Record):
    model_cls = OaiRecordMetadata

    schema = ConstantField("$schema", "local://oai_record-1.0.0.json")

    index = IndexField("oai_record-oai_record-1.0.0")

    pid = PIDField(
        provider=OaiRecordIdProvider, context_cls=PIDFieldContext, create=True
    )

    dumper_extensions = []
    dumper = OaiRecordDumper(extensions=dumper_extensions)

    relations = RelationsField(
        batch=PIDRelation(
            "batch",
            keys=["id"],
            pid_field=OaiBatchRecord.pid,
        ),
    )

from invenio_pidstore.providers.recordid_v2 import RecordIdProviderV2
from invenio_records.systemfields import ConstantField, RelationsField
from invenio_records_resources.records.api import Record
from invenio_records_resources.records.systemfields import IndexField
from invenio_records_resources.records.systemfields.pid import PIDField, PIDFieldContext
from oarepo_runtime.relations import InternalRelation, PIDRelation, RelationsField

from oarepo_oaipmh_harvester.oai_batch.records.dumper import OaiBatchDumper
from oarepo_oaipmh_harvester.oai_batch.records.models import OaiBatchMetadata
from oarepo_oaipmh_harvester.oai_run.records.api import OaiRunRecord


class OaiBatchRecord(Record):
    model_cls = OaiBatchMetadata

    schema = ConstantField("$schema", "local://oai_batch-1.0.0.json")

    index = IndexField("oai_batch-oai_batch-1.0.0")

    pid = PIDField(
        create=True, provider=RecordIdProviderV2, context_cls=PIDFieldContext
    )

    dumper_extensions = []
    dumper = OaiBatchDumper(extensions=dumper_extensions)

    relations = RelationsField(
        run=PIDRelation(
            "run",
            keys=["id"],
            pid_field=OaiRunRecord.pid,
        ),
    )

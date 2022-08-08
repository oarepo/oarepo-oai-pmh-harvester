from invenio_pidstore.providers.recordid_v2 import RecordIdProviderV2
from invenio_records.systemfields import ConstantField
from invenio_records_resources.records.api import Record as InvenioBaseRecord
from invenio_records_resources.records.systemfields import IndexField
from invenio_records_resources.records.systemfields.pid import (
    PIDField, PIDFieldContext)
from oarepo_oaipmh_harvester.oaipmh_batch.records.dumper import OaipmhBatchDumper
from oarepo_oaipmh_harvester.oaipmh_batch.records.models import OaipmhBatchMetadata


class OaipmhBatchRecord(InvenioBaseRecord):
    model_cls = OaipmhBatchMetadata
    schema = ConstantField("$schema", "local://oaipmh-batch-1.0.0.json")
    index = IndexField("oaipmh_batch-oaipmh-batch-1.0.0")
    pid = PIDField(
        create=True,
        provider=RecordIdProviderV2,
        context_cls = PIDFieldContext
    )
    dumper_extensions = []
    dumper = OaipmhBatchDumper(extensions=dumper_extensions)
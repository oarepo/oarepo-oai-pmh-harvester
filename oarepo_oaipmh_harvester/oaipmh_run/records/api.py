from invenio_pidstore.providers.recordid_v2 import RecordIdProviderV2
from invenio_records.systemfields import ConstantField
from invenio_records_resources.records.api import Record as InvenioBaseRecord
from invenio_records_resources.records.systemfields import IndexField
from invenio_records_resources.records.systemfields.pid import (
    PIDField, PIDFieldContext)
from oarepo_oaipmh_harvester.oaipmh_run.records.dumper import OaipmhRunDumper
from oarepo_oaipmh_harvester.oaipmh_run.records.models import OaipmhRunMetadata


class OaipmhRunRecord(InvenioBaseRecord):
    model_cls = OaipmhRunMetadata
    schema = ConstantField("$schema", "local://oaipmh-run-1.0.0.json")
    index = IndexField("oaipmh_run-oaipmh-run-1.0.0")
    pid = PIDField(
        create=True,
        provider=RecordIdProviderV2,
        context_cls = PIDFieldContext
    )
    dumper_extensions = []
    dumper = OaipmhRunDumper(extensions=dumper_extensions)
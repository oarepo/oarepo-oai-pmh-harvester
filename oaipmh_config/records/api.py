from invenio_pidstore.providers.recordid_v2 import RecordIdProviderV2
from invenio_records.systemfields import ConstantField
from invenio_records_resources.records.api import Record as InvenioBaseRecord
from invenio_records_resources.records.systemfields import IndexField
from invenio_records_resources.records.systemfields.pid import (
    PIDField, PIDFieldContext)
from oaipmh_config.records.dumper import OaipmhConfigDumper
from oaipmh_config.records.models import OaipmhConfigMetadata


class OaipmhConfigRecord(InvenioBaseRecord):
    model_cls = OaipmhConfigMetadata
    schema = ConstantField("$schema", "http://localhost/schemas/oaipmh-config-1.0.0.json")
    index = IndexField("oaipmh_config-oaipmh-config-1.0.0")
    pid = PIDField(
        create=True,
        provider=RecordIdProviderV2,
        context_cls = PIDFieldContext
    )
    dumper_extensions = []
    dumper = OaipmhConfigDumper(extensions=dumper_extensions)
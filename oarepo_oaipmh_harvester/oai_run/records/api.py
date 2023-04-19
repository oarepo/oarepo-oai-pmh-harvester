from invenio_pidstore.providers.recordid_v2 import RecordIdProviderV2
from invenio_records.systemfields import ConstantField
from invenio_records_resources.records.api import Record
from invenio_records_resources.records.systemfields import IndexField
from invenio_records_resources.records.systemfields.pid import PIDField, PIDFieldContext

from oarepo_oaipmh_harvester.oai_run.records.dumper import OaiRunDumper
from oarepo_oaipmh_harvester.oai_run.records.models import OaiRunMetadata


class OaiRunIdProvider(RecordIdProviderV2):
    pid_type = "_rn"


class OaiRunRecord(Record):
    model_cls = OaiRunMetadata

    schema = ConstantField("$schema", "local://oai_run-1.0.0.json")

    index = IndexField("oai_run-oai_run-1.0.0")

    pid = PIDField(provider=OaiRunIdProvider, context_cls=PIDFieldContext, create=True)

    dumper_extensions = []
    dumper = OaiRunDumper(extensions=dumper_extensions)

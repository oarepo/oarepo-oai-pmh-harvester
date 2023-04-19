from invenio_pidstore.providers.recordid_v2 import RecordIdProviderV2
from invenio_records.systemfields import ConstantField
from invenio_records_resources.records.api import Record
from invenio_records_resources.records.systemfields import IndexField
from invenio_records_resources.records.systemfields.pid import PIDField, PIDFieldContext

from oarepo_oaipmh_harvester.oai_harvester.records.dumper import OaiHarvesterDumper
from oarepo_oaipmh_harvester.oai_harvester.records.models import OaiHarvesterMetadata


class OaiHarvesterIdProvider(RecordIdProviderV2):
    pid_type = "_hrstr"


class OaiHarvesterRecord(Record):
    model_cls = OaiHarvesterMetadata

    schema = ConstantField("$schema", "local://oai_harvester-1.0.0.json")

    index = IndexField("oai_harvester-oai_harvester-1.0.0")

    pid = PIDField(
        provider=OaiHarvesterIdProvider, context_cls=PIDFieldContext, create=True
    )

    dumper_extensions = []
    dumper = OaiHarvesterDumper(extensions=dumper_extensions)

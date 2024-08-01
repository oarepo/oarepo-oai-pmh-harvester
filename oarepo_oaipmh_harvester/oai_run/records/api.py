from invenio_pidstore.providers.recordid_v2 import RecordIdProviderV2
from invenio_records.systemfields import ConstantField
from invenio_records_resources.records.api import Record as InvenioRecord
from invenio_records_resources.records.systemfields import IndexField
from invenio_records_resources.records.systemfields.pid import PIDField, PIDFieldContext
from oarepo_runtime.records.relations import PIDRelation, RelationsField

from oarepo_oaipmh_harvester.oai_harvester.records.api import OaiHarvesterRecord
from oarepo_oaipmh_harvester.oai_run.records.dumpers.dumper import OaiRunDumper
from oarepo_oaipmh_harvester.oai_run.records.models import OaiRunMetadata


class OaiRunIdProvider(RecordIdProviderV2):
    pid_type = "oairun"


class OaiRunRecord(InvenioRecord):

    model_cls = OaiRunMetadata

    schema = ConstantField("$schema", "local://oai_run-1.0.0.json")

    index = IndexField(
        "oarepo-oaipmh-run-oai_run-1.0.0",
    )

    pid = PIDField(provider=OaiRunIdProvider, context_cls=PIDFieldContext, create=True)

    dumper = OaiRunDumper()

    relations = RelationsField(
        harvester=PIDRelation(
            "harvester",
            keys=["id", "code", "name"],
            pid_field=OaiHarvesterRecord.pid,
        ),
    )

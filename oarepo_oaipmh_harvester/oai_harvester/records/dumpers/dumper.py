from oarepo_runtime.records.dumpers import SearchDumper

from oarepo_oaipmh_harvester.oai_harvester.records.dumpers.edtf import (
    OaiHarvesterEDTFIntervalDumperExt,
)


class OaiHarvesterDumper(SearchDumper):
    """OaiHarvesterRecord opensearch dumper."""

    extensions = [OaiHarvesterEDTFIntervalDumperExt()]

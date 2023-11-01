from oarepo_runtime.records.dumpers import SearchDumper

from oarepo_oaipmh_harvester.oai_run.records.dumpers.edtf import (
    OaiRunEDTFIntervalDumperExt,
)


class OaiRunDumper(SearchDumper):
    """OaiRunRecord opensearch dumper."""

    extensions = [OaiRunEDTFIntervalDumperExt()]

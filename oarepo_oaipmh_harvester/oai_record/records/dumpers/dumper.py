from oarepo_runtime.records.dumpers import SearchDumper

from oarepo_oaipmh_harvester.oai_record.records.dumpers.edtf import (
    OaiRecordEDTFIntervalDumperExt,
)


class OaiRecordDumper(SearchDumper):
    """OaiRecord opensearch dumper."""

    extensions = [OaiRecordEDTFIntervalDumperExt()]

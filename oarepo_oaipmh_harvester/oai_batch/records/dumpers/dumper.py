from oarepo_runtime.records.dumpers import SearchDumper

from oarepo_oaipmh_harvester.oai_batch.records.dumpers.edtf import (
    OaiBatchEDTFIntervalDumperExt,
)


class OaiBatchDumper(SearchDumper):
    """OaiBatchRecord opensearch dumper."""

    extensions = [OaiBatchEDTFIntervalDumperExt()]

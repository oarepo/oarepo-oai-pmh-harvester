import datetime
from typing import Iterator

from oarepo_runtime.datastreams import BaseReader, StreamEntry
from sickle import Sickle
from sickle.oaiexceptions import NoRecordsMatch
import pytz


class SickleReader(BaseReader):
    def __init__(
        self,
        *,
        all_records=None,
        identifiers=None,
        config=None,
        source=None,
        start_from=None,
        base_path=None,
        oai_run=None,
        **kwargs,
    ):
        # we are handling url, so ignore the base path
        super().__init__(source=source, base_path=None, **kwargs)
        self.all_records = all_records
        self.identifiers = identifiers
        self.config = config
        self.start_from = start_from
        self.oai_run = oai_run

    def __iter__(self) -> Iterator[StreamEntry]:
        request = Sickle(self.source, encoding="utf-8")

        dates = {"from": self.start_from, "until": None}
        setspecs = (self.config["setspecs"] or "").split() or [None]

        for spec in setspecs:
            count = 0

            metadata_prefix = self.config["metadataprefix"] or "oai_dc"
            params = {"metadataPrefix": metadata_prefix}

            params.update(dates)
            if spec:
                params["set"] = spec

            if self.identifiers:

                def record_getter():
                    for identifier in self.identifiers:
                        yield request.GetRecord(
                            identifier=identifier, metadataPrefix=metadata_prefix
                        )

            else:

                def record_getter():
                    yield from request.ListRecords(**params)

            try:
                first_real_datestamp = None
                for record in record_getter():
                    datestamp = record.header.datestamp
                    datestamp = expand_datestamp(datestamp)
                    if first_real_datestamp is None:
                        first_real_datestamp = record.header.datestamp
                    count += 1
                    if (
                        self.config.get("max_records")
                        and count > self.config["max_records"]
                        and record.header.datestamp != first_real_datestamp
                    ):
                        break

                    yield StreamEntry(
                        entry=record.raw,
                        context={
                            "oai": {
                                "metadata": record.metadata
                                if hasattr(record, "metadata")
                                else {},
                                "datestamp": datestamp,
                                "deleted": record.header.deleted,
                                "identifier": record.header.identifier,
                                "setSpecs": record.header.setSpecs,
                            },
                            "oai_run": self.oai_run,
                        },
                    )

            except NoRecordsMatch:
                continue


def expand_datestamp(datestamp):
    if "T" not in datestamp:
        datestamp += "T00:00:00+00:00"
    elif datestamp.endswith("Z") or datestamp.endswith("z"):
        datestamp = datestamp[:-1] + "+00:00"
    elif "+" not in datestamp:
        datestamp += "+00:00"
    return datetime.datetime.fromisoformat(datestamp).astimezone(pytz.utc).isoformat()

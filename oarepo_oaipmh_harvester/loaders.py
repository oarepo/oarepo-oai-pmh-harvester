import gzip
import json
import pathlib
from typing import Union, List

from sickle import Sickle
from sickle.oaiexceptions import NoRecordsMatch

from oarepo_oaipmh_harvester.models import OAIHarvesterConfig


def sickle_loader(harvester: OAIHarvesterConfig, start_from: str, identifiers: Union[List[str], None] = None):
    request = Sickle(harvester.baseurl, encoding='utf-8')

    dates = {
        'from': start_from,
        'until': None
    }
    setspecs = (harvester.setspecs or '').split() or [None]

    for spec in setspecs:
        count = 0
        records = []

        metadata_prefix = harvester.metadataprefix or "oai_dc"
        params = {
            'metadataPrefix': metadata_prefix
        }

        params.update(dates)
        if spec:
            params['set'] = spec

        if identifiers:
            def record_getter():
                for identifier in identifiers:
                    yield request.GetRecord(identifier=identifier, metadataPrefix=metadata_prefix)
        else:
            def record_getter():
                yield from request.ListRecords(**params)

        try:
            first_real_datestamp = None
            for record in record_getter():
                if first_real_datestamp is None:
                    first_real_datestamp = record.header.datestamp
                records.append(record)
                count += 1
                if count > max_records and record.header.datestamp != first_real_datestamp:
                    break
                if len(records) >= harvester.batch_size:
                    yield records
                    records = []

        except NoRecordsMatch:
            continue

        if records:
            yield records


def filesystem_loader(harvester: OAIHarvesterConfig, path, identifiers=None):
    path = pathlib.Path(path)
    files = list(sorted(set(path.glob("*.json.gz"))))
    records = []
    for fpath in files:
        if identifiers:
            for ident in identifiers:
                if str(fpath).endswith(ident):
                    break
            else:
                continue
        with gzip.open(fpath, 'rt') as f:
            for rec in json.load(f):
                records.append(rec)
                if len(records) >= harvester.batch_size:
                    yield records
                    records = []
    if records:
        yield records

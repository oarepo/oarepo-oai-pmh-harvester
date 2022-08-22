import gzip
import json
from pathlib import Path

from oarepo_oaipmh_harvester.parsers import MarcxmlParser
from sickle import Sickle
from tqdm import tqdm


def list_records():
    request = Sickle('https://invenio.nusl.cz/oai2d/', encoding='utf-8', verify=False)
    recs = []
    parser = MarcxmlParser(None)
    params = {
        'set': "etds_all",
        'metadataPrefix': "marcxml",
        'from': '1970-01-01'
    }
    for rec in request.ListRecords(**params):
        recs.append(parser.parse(rec))
        if len(recs) == 500:
            yield recs
            recs = []
    if recs:
        yield recs


if __name__ == '__main__':
    parent = Path.cwd().absolute().parent.parent / 'nusl-theses-data'
    parent.mkdir(parents=True, exist_ok=True)
    print(parent)
    for idx, records in tqdm(enumerate(list_records())):
        with gzip.open(parent / f'{idx:08d}.json.gz', 'wt') as f:
            json.dump(records, f, indent=4, ensure_ascii=False)

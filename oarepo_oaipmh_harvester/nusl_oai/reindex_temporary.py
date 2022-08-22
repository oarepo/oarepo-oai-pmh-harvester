from elasticsearch import VERSION as ES_VERSION
from elasticsearch.helpers import bulk
from elasticsearch.helpers import expand_action as default_expand_action
from flask import current_app
from invenio_app.factory import create_app

from tqdm import tqdm

BS = 500


def load_pids(pidtype):
    from invenio_pidstore.models import PersistentIdentifier
    batch = []
    for pid in PersistentIdentifier.query.filter_by(pid_type=pidtype):
        batch.append(pid)
        if len(batch) >= BS:
            yield batch
            batch = []
    if batch:
        yield batch


def total_pids(pidtype):
    from invenio_pidstore.models import PersistentIdentifier
    return PersistentIdentifier.query.filter_by(pid_type=pidtype).count()


def get_index_action(indexer, record):
    index, doc_type = indexer.record_to_index(record)
    arguments = {}
    body = indexer._prepare_record(record, index, doc_type, arguments)
    index, doc_type = indexer._prepare_index(index, doc_type)

    action = {
        '_op_type': 'index',
        '_index': index,
        '_id': str(record.id),
        '_version': record.revision_id,
        '_version_type': indexer._version_type,
        '_source': body
    }
    action.update(arguments)
    return action


def index_records(pidtype):
    from invenio_indexer.utils import _es7_expand_action
    from nr_theses_metadata.proxies import current_service
    from nr_theses_metadata.records.api import NrThesesMetadataRecord

    req_timeout = current_app.config['INDEXER_BULK_REQUEST_TIMEOUT']

    total_ok  = 0
    total_err = 0
    with tqdm(unit=' records', total=total_pids(pidtype)) as p:
        for pid_batch in load_pids(pidtype):
            record_uuids = [
                x.object_uuid for x in pid_batch
            ]
            records = NrThesesMetadataRecord.get_records(record_uuids)
            prepared_actions = [
                get_index_action(current_service.indexer, r)
                for r in records
            ]

            ok, err = bulk(
                current_service.indexer.client,
                prepared_actions,
                stats_only=True,
                request_timeout=req_timeout,
                expand_action_callback=(
                    _es7_expand_action if ES_VERSION[0] >= 7
                    else default_expand_action
                )
            )
            total_ok += ok
            total_err += err

            p.update(len(prepared_actions))
    print(f"Total ok  : {total_ok}")
    print(f"Total err : {total_err}")

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        index_records('recid')

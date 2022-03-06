from flask import current_app
from invenio_records_resources.services.uow import UnitOfWork, RecordCommitOp
from invenio_indexer.utils import _es7_expand_action
from elasticsearch import VERSION as ES_VERSION
from elasticsearch.helpers import bulk
from elasticsearch.helpers import expand_action as default_expand_action


class BulkRecordCommitOp(RecordCommitOp):
    def __init__(self, rc: RecordCommitOp):
        super().__init__(rc._record, rc._indexer, rc._index_refresh)
        self._previous = rc

    def on_register(self, uow):
        self._previous.on_register(uow)

    def on_commit(self, uow):
        """Run the operation."""
        pass

    def get_index_action(self):
        index, doc_type = self._indexer.record_to_index(self._record)
        arguments = {}
        body = self._indexer._prepare_record(self._record, index, doc_type, arguments)
        index, doc_type = self._indexer._prepare_index(index, doc_type)

        action = {
            '_op_type': 'index',
            '_index': index,
            '_id': str(self._record.id),
            '_version': self._record.revision_id,
            '_version_type': self._indexer._version_type,
            '_source': body
        }
        action.update(arguments)
        return action


class BulkUnitOfWork(UnitOfWork):

    def register(self, op):
        if isinstance(op, RecordCommitOp):
            op = BulkRecordCommitOp(op)
        return super().register(op)

    def commit(self):
        super().commit()
        # do bulk indexing
        bulk_data = []
        indexer = None
        for op in self._operations:
            if isinstance(op, BulkRecordCommitOp):
                indexer = op._indexer
                bulk_data.append(op.get_index_action())
        if indexer:
            req_timeout = current_app.config['INDEXER_BULK_REQUEST_TIMEOUT']
            resp = bulk(
                indexer.client,
                bulk_data,
                stats_only=True,
                request_timeout=req_timeout,
                expand_action_callback=(
                    _es7_expand_action if ES_VERSION[0] >= 7
                    else default_expand_action
                ),
                refresh=True
            )


__all__ = ['BulkUnitOfWork']

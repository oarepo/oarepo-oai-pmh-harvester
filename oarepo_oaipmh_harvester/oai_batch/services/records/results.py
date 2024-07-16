from oarepo_runtime.services.results import RecordItem, RecordList


class OaiBatchRecordItem(RecordItem):
    """OaiBatchRecord record item."""

    components = [*RecordItem.components]


class OaiBatchRecordList(RecordList):
    """OaiBatchRecord record list."""

    components = [*RecordList.components]

from oarepo_runtime.services.results import RecordItem, RecordList


class OaiRecordRecordItem(RecordItem):
    """OaiRecord record item."""

    components = [*RecordItem.components]


class OaiRecordRecordList(RecordList):
    """OaiRecord record list."""

    components = [*RecordList.components]

from oarepo_runtime.services.results import RecordItem, RecordList


class OaiRunRecordItem(RecordItem):
    """OaiRunRecord record item."""

    components = [*RecordItem.components]


class OaiRunRecordList(RecordList):
    """OaiRunRecord record list."""

    components = [*RecordList.components]

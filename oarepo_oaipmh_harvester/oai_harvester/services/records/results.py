from oarepo_runtime.services.results import RecordItem, RecordList


class OaiHarvesterRecordItem(RecordItem):
    """OaiHarvesterRecord record item."""

    components = [*RecordItem.components]


class OaiHarvesterRecordList(RecordList):
    """OaiHarvesterRecord record list."""

    components = [*RecordList.components]

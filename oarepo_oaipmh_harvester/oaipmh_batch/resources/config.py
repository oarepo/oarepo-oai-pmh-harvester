from invenio_records_resources.resources import \
    RecordResourceConfig as InvenioRecordResourceConfig


class OaipmhBatchResourceConfig(InvenioRecordResourceConfig):
    """OaipmhBatchRecord resource config."""

    blueprint_name = 'OaipmhBatch'
    url_prefix = '/oaipmh_batch/'
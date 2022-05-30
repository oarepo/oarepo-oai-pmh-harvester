from invenio_records_resources.resources import \
    RecordResourceConfig as InvenioRecordResourceConfig


class OaipmhRunResourceConfig(InvenioRecordResourceConfig):
    """OaipmhRunRecord resource config."""

    blueprint_name = 'OaipmhRun'
    url_prefix = '/oaipmh_run/'
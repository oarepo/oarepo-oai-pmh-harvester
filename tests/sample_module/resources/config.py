from invenio_records_resources.resources import \
    RecordResourceConfig as InvenioRecordResourceConfig


class OaipmhRecordResourceConfig(InvenioRecordResourceConfig):
    """OaipmhRecordRecord resource config."""

    blueprint_name = 'OaipmhRecord'
    url_prefix = '/oaipmh_record/'
from invenio_records_resources.resources import \
    RecordResourceConfig as InvenioRecordResourceConfig


class OaipmhConfigResourceConfig(InvenioRecordResourceConfig):
    """OaipmhConfigRecord resource config."""

    blueprint_name = 'OaipmhConfig'
    url_prefix = '/oaipmh_config/'
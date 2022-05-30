from invenio_records.dumpers import \
    ElasticsearchDumper as InvenioElasticsearchDumper


class OaipmhConfigDumper(InvenioElasticsearchDumper):
    """OaipmhConfigRecord elasticsearch dumper."""
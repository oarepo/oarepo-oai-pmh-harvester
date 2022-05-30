from invenio_records.dumpers import \
    ElasticsearchDumper as InvenioElasticsearchDumper


class OaipmhBatchDumper(InvenioElasticsearchDumper):
    """OaipmhBatchRecord elasticsearch dumper."""
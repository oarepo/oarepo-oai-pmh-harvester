from invenio_records.dumpers import \
    ElasticsearchDumper as InvenioElasticsearchDumper


class OaipmhRunDumper(InvenioElasticsearchDumper):
    """OaipmhRunRecord elasticsearch dumper."""
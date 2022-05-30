from invenio_records.dumpers import \
    ElasticsearchDumper as InvenioElasticsearchDumper


class OaipmhRecordDumper(InvenioElasticsearchDumper):
    """OaipmhRecordRecord elasticsearch dumper."""
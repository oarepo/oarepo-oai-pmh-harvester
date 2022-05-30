"""Facet definitions."""

from elasticsearch_dsl import Facet
from elasticsearch_dsl.query import Nested
from invenio_records_resources.services.records.facets import TermsFacet


class NestedLabeledFacet(Facet):
    agg_type = "nested"

    def __init__(self, path, nested_facet, label = ''):
        self._path = path
        self._inner = nested_facet
        self._label = label
        super(NestedLabeledFacet, self).__init__(
            path=path,  aggs={"inner": nested_facet.get_aggregation(),}
        )

    def get_values(self, data, filter_values):
        return self._inner.get_values(data.inner, filter_values)

    def add_filter(self, filter_values):
        inner_q = self._inner.add_filter(filter_values)
        if inner_q:
            return Nested(path=self._path, query=inner_q)

    def get_labelled_values(self, data, filter_values):
        """Get a labelled version of a bucket."""
        try:
            out = data['buckets']
        except:
            out = []
        return {'buckets': out, 'label': str(self._label)}



metadata_code = TermsFacet(field = "metadata.code")



metadata_baseurl = TermsFacet(field = "metadata.baseurl")



metadata_metadataprefix = TermsFacet(field = "metadata.metadataprefix")



metadata_name = TermsFacet(field = "metadata.name")



metadata_max_records = TermsFacet(field = "metadata.max_records")



metadata_batch_size = TermsFacet(field = "metadata.batch_size")



_id = TermsFacet(field = "id")



created = TermsFacet(field = "created")



updated = TermsFacet(field = "updated")



_schema = TermsFacet(field = "$schema")
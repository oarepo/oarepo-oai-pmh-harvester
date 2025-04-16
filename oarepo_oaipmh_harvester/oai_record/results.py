"""Results for the oai_records service."""

from invenio_records_resources.services.records.results import RecordItem, RecordList


class OAIRecordItem(RecordItem):
    """Single OAI Run result."""

    def __init__(
        self,
        service,
        identity,
        oai_record,
        errors=None,
        links_tpl=None,
        schema=None,
        **kwargs,
    ):
        """Constructor."""
        self._data = None
        self._errors = errors
        self._identity = identity
        self._oai_record = oai_record
        self._service = service
        self._links_tpl = links_tpl
        self._schema = schema or service.schema

    @property
    def id(self):
        """Identity of the oai_record."""
        return str(self._oai_record.id)

    def __getitem__(self, key):
        """Key a key from the data."""
        return self.data[key]

    @property
    def links(self):
        """Get links for this result item."""
        return self._links_tpl.expand(self._identity, self._oai_record)

    @property
    def _obj(self):
        """Return the object to dump."""
        return self._oai_record

    @property
    def data(self):
        """Property to get the oai_record."""
        if self._data:
            return self._data

        self._data = self._schema.dump(
            self._obj,
            context={
                "identity": self._identity,
                "record": self._oai_record,
            },
        )

        if self._links_tpl:
            self._data["links"] = self.links

        return self._data

    @property
    def errors(self):
        """Get the errors."""
        return self._errors

    def to_dict(self):
        """Get a dictionary for the oai_record."""
        res = self.data
        if self._errors:
            res["errors"] = self._errors
        return res


class OAIRecordList(RecordList):
    """List of OAI Run results."""

    @property
    def hits(self):
        """Iterator over the hits."""
        oai_record_cls = self._service.record_cls

        for hit in self._results:
            # load dump
            oai_record = oai_record_cls.loads(hit.to_dict())
            schema = self._service.schema

            # project the oai_record
            projection = schema.dump(
                oai_record,
                context={
                    "identity": self._identity,
                    "record": oai_record,
                },
            )

            # inject the links
            if self._links_item_tpl:
                projection["links"] = self._links_item_tpl.expand(
                    self._identity, oai_record
                )

            yield projection

    def to_dict(self):
        """Return result as a dictionary."""
        # TODO: This part should imitate the result item above. I.e. add a
        # "data" property which uses a ServiceSchema to dump the entire object.
        res = {
            "hits": {
                "hits": list(self.hits),
                "total": self.total,
            }
        }

        if self.aggregations:
            res["aggregations"] = self.aggregations

        if self._params:
            res["sortBy"] = self._params["sort"]
            if self._links_tpl:
                res["links"] = self._links_tpl.expand(self._identity, self.pagination)

        return res

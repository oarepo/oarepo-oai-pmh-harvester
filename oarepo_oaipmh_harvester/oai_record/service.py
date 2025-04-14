from invenio_db import db
from invenio_records_resources.resources.errors import PermissionDeniedError
from invenio_records_resources.services import (
    RecordService,
    RecordServiceConfig,
    pagination_links,
)
from invenio_records_resources.services.base.config import (
    ConfiguratorMixin,
    FromConfig,
    SearchOptionsMixin,
)
from invenio_records_resources.services.records.config import SearchOptions
from invenio_records_resources.services.records.params import (
    FacetsParam,
    PaginationParam,
    QueryStrParam,
    SortParam,
)
from invenio_records_resources.services.records.queryparser import (
    SuggestQueryParser,
)
from invenio_users_resources.services.common import Link

from ..models import OAIHarvestedRecord
from ..permissions import OAIRecordPermissionPolicy
from . import facets
from .api import OAIRecordAggregate
from .results import OAIRecordItem, OAIRecordList
from .schema import OAIHarvestedRecordSchema


class OAIRecordSearchOptions(SearchOptions, SearchOptionsMixin):
    """Search options."""

    pagination_options = {
        "default_results_per_page": 10,
        "default_max_results": 10,
    }

    suggest_parser_cls = SuggestQueryParser.factory(
        fields=["oai_identifier^2", "harvester_id^2", "title^3"],
        type="most_fields",
        fuzziness="AUTO",
    )

    params_interpreters_cls = [
        QueryStrParam,
        SortParam,
        PaginationParam,
        FacetsParam,
    ]

    facets = {
        "harvester": facets.harvester,
        "deleted": facets.deleted,
        "has_errors": facets.has_errors,
    }


class OAIRecordServiceConfig(RecordServiceConfig, ConfiguratorMixin):
    """Requests service configuration."""

    # common configuration
    permission_policy_cls = OAIRecordPermissionPolicy
    result_item_cls = OAIRecordItem
    result_list_cls = OAIRecordList

    search = OAIRecordSearchOptions

    service_id = "oai-harvest-record"
    record_cls = OAIRecordAggregate
    schema = FromConfig("OAI_RECORD_SERVICE_SCHEMA", OAIHarvestedRecordSchema)
    indexer_queue_name = "oai-harvest-record"
    index_dumper = None

    # links configuration
    links_item = {
        "self": Link("{+api}/oai/harvest/records/{id}"),
    }
    links_search = pagination_links("{+api}/oai/harvest/records{?args*}")

    components = []


class OAIRecordService(RecordService):
    """Users service."""

    @property
    def oai_record_cls(self):
        """Alias for record_cls."""
        return self.record_cls

    def search(
        self,
        identity,
        params=None,
        search_preference=None,
        extra_filters=None,
        **kwargs,
    ):
        """Search for oai_records."""
        self.require_permission(identity, "search")

        return super().search(
            identity,
            params=params,
            search_preference=search_preference,
            search_opts=self.config.search,
            permission_action="read",
            extra_filter=extra_filters,
            **kwargs,
        )

    def read(self, identity, id_):
        """Retrieve a oai_record."""
        # resolve and require permission
        oai_record = OAIRecordAggregate.get_record(id_)
        if oai_record is None:
            raise PermissionDeniedError()

        self.require_permission(identity, "read", record=oai_record)

        # record components
        for component in self.components:
            if hasattr(component, "read"):
                component.read(identity, oai_record=oai_record)

        return self.result_item(
            self, identity, oai_record, links_tpl=self.links_item_tpl
        )

    def rebuild_index(self, identity, uow=None):
        """Reindex all oai_records managed by this service."""
        oai_records = db.session.query(OAIHarvestedRecord.id).yield_per(1000)
        self.indexer.bulk_index([u.id for u in oai_records])
        return True

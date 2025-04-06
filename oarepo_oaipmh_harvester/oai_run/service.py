from invenio_db import db
from invenio_i18n import lazy_gettext as _
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
from invenio_records_resources.services.records.facets.facets import TermsFacet
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

from ..models import OAIHarvesterRun
from .api import OAIRunAggregate
from .permissions import OAIRunPermissionPolicy
from .results import OAIRunItem, OAIRunList
from .schema import OAIHarvesterRunSchema


class OAIRunSearchOptions(SearchOptions, SearchOptionsMixin):
    """Search options."""

    pagination_options = {
        "default_results_per_page": 10,
        "default_max_results": 10,
    }

    suggest_parser_cls = SuggestQueryParser.factory(
        fields=["id^2", "harvester_id^2", "title^3"],
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
        "harvester": TermsFacet(field="harvester_id", label=_("Harvester ID")),
        "manual": TermsFacet(
            field="manual",
            label=_("Run type"),
            value_labels={True: _("Manual"), False: _("Automatic")},
        ),
        "status": TermsFacet(
            field="status",
            label=_("Status"),
            value_labels={
                "running": _("Harvest running"),
                "finishing": _("Harvest finishing"),
                "finished": _("Harvest finished"),
                "failed": _("Harvest failed"),
                "stopped": _("Harvest stopped"),
            },
        ),
    }


class OAIRunServiceConfig(RecordServiceConfig, ConfiguratorMixin):
    """Requests service configuration."""

    # common configuration
    permission_policy_cls = OAIRunPermissionPolicy
    result_item_cls = OAIRunItem
    result_list_cls = OAIRunList

    search = OAIRunSearchOptions

    service_id = "oai-harvest-run"
    record_cls = OAIRunAggregate
    schema = FromConfig("USERS_RESOURCES_SERVICE_SCHEMA", OAIHarvesterRunSchema)
    indexer_queue_name = "oai-harvest-run"
    index_dumper = None

    # links configuration
    links_item = {
        "self": Link("{+api}/oai/harvest/run/{id}"),
    }
    links_search = pagination_links("{+api}/oai/harvest/run{?args*}")

    components = []


class OAIRunService(RecordService):
    """Users service."""

    @property
    def oai_run_cls(self):
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
        """Search for oai_runs."""
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
        """Retrieve a oai_run."""
        # resolve and require permission
        oai_run = OAIRunAggregate.get_record(id_)
        if oai_run is None:
            raise PermissionDeniedError()

        self.require_permission(identity, "read", record=oai_run)

        # run components
        for component in self.components:
            if hasattr(component, "read"):
                component.read(identity, oai_run=oai_run)

        return self.result_item(self, identity, oai_run, links_tpl=self.links_item_tpl)

    def rebuild_index(self, identity, uow=None):
        """Reindex all oai_runs managed by this service."""
        oai_runs = db.session.query(OAIHarvesterRun.id).yield_per(1000)
        self.indexer.bulk_index([u.id for u in oai_runs])
        return True

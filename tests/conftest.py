import pytest
from invenio_app.factory import create_app as _create_app
from invenio_records_permissions.generators import (
    AnyUser,
)
from oarepo_communities.services.permissions.policy import (
    CommunityDefaultWorkflowPermissions,
)
from oarepo_workflows import (
    Workflow,
    WorkflowRequestPolicy,
)


@pytest.fixture(scope="module")
def extra_entry_points():
    """Extra entry points to load the mock_module features."""
    return {"invenio_i18n.translations": ["1000-test = tests"]}


class DefaultWorkflowPermissions(CommunityDefaultWorkflowPermissions):
    can_create = [AnyUser()]


class DefaultWorkflowRequests(WorkflowRequestPolicy):
    pass


@pytest.fixture(scope="module")
def app_config(app_config):
    app_config["I18N_LANGUAGES"] = [("cs", "Czech")]
    app_config["BABEL_DEFAULT_LOCALE"] = "en"
    app_config["RECORDS_REFRESOLVER_CLS"] = (
        "invenio_records.resolver.InvenioRefResolver"
    )
    app_config["RECORDS_REFRESOLVER_STORE"] = (
        "invenio_jsonschemas.proxies.current_refresolver_store"
    )

    app_config["DATASTREAMS_READERS"] = {
        "file": "tests.datastreams:MockOAIReader",
        "test_data": "tests.datastreams:TestDataOAIReader",
    }
    app_config["DATASTREAMS_TRANSFORMERS"] = {
        "error_transformer": "tests.datastreams:ErrorTransformer"
    }
    app_config["WORKFLOWS"] = {
        "default": Workflow(
            label="Default workflow",
            permission_policy_cls=DefaultWorkflowPermissions,
            request_policy_cls=DefaultWorkflowRequests,
        )
    }
    app_config.update(
        dict(
            INVENIO_RDM_ENABLED=True,
            RDM_PERSISTENT_IDENTIFIERS={},
            RDM_USER_MODERATION_ENABLED=False,
            RDM_RECORDS_ALLOW_RESTRICTION_AFTER_GRACE_PERIOD=False,
            RDM_ALLOW_METADATA_ONLY_RECORDS=True,
            RDM_DEFAULT_FILES_ENABLED=False,
            RDM_SEARCH_SORT_BY_VERIFIED=False,
            DATACITE_TEST_MODE=True,
            RDM_ARCHIVE_DOWNLOAD_ENABLED=False,
        )
    )
    # app_config["SQLALCHEMY_ENGINE_OPTIONS"] = {"echo": True}
    return app_config


@pytest.fixture(scope="module")
def create_app(instance_path, entry_points):
    """Application factory fixture."""
    return _create_app


@pytest.fixture
def default_community(app, db, location):
    from invenio_access.permissions import system_identity
    from invenio_communities.proxies import current_communities

    current_communities.service.create(
        system_identity,
        {
            "slug": "default",
            "metadata": {"title": "Default community"},
            "access": {"visibility": "public"},
        },
    )
    db.session.commit()


@pytest.fixture
def mappings():
    # update the mappings
    from oarepo_runtime.services.custom_fields.mappings import prepare_cf_indices

    prepare_cf_indices()

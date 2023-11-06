import pytest
from invenio_access.permissions import system_identity
from invenio_app.factory import create_app as _create_app


@pytest.fixture(scope="module")
def extra_entry_points():
    """Extra entry points to load the mock_module features."""
    return {"invenio_i18n.translations": ["1000-test = tests"]}


@pytest.fixture(scope="module")
def app_config(app_config):
    app_config["I18N_LANGUAGES"] = [("cs", "Czech")]
    app_config["BABEL_DEFAULT_LOCALE"] = "en"
    app_config[
        "RECORDS_REFRESOLVER_CLS"
    ] = "invenio_records.resolver.InvenioRefResolver"
    app_config[
        "RECORDS_REFRESOLVER_STORE"
    ] = "invenio_jsonschemas.proxies.current_refresolver_store"

    app_config["DATASTREAMS_READERS"] = {
        "file": "tests.datastreams:MockOAIReader",
        "test_data": "tests.datastreams:TestDataOAIReader",
    }
    app_config["DATASTREAMS_TRANSFORMERS"] = {
        "error_transformer": "tests.datastreams:ErrorTransformer"
    }
    # app_config["SQLALCHEMY_ENGINE_OPTIONS"] = {"echo": True}
    return app_config


@pytest.fixture(scope="module")
def create_app(instance_path, entry_points):
    """Application factory fixture."""
    return _create_app


@pytest.fixture(scope="module")
def record_service(app):
    from .model import ModelService, ModelServiceConfig

    service = ModelService(ModelServiceConfig())
    sregistry = app.extensions["invenio-records-resources"].registry
    sregistry.register(service, service_id="simple_model")
    return service


@pytest.fixture
def simple_record(app, db, search_clear, record_service):
    from .model import ModelRecord

    record = record_service.create(
        system_identity,
        {},
    )
    ModelRecord.index.refresh()
    return record

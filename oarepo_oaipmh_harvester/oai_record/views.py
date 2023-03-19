from flask import Blueprint


def create_blueprint_from_app_oai_record(app):
    """Create  blueprint."""
    blueprint = app.extensions["oarepo-oaipmh-record"].resource.as_blueprint()
    blueprint.record_once(init_create_blueprint_from_app_oai_record)

    # calls record_once for all other functions starting with "init_addons_"
    # https://stackoverflow.com/questions/58785162/how-can-i-call-function-with-string-value-that-equals-to-function-name
    funcs = globals()
    funcs = [
        v
        for k, v in funcs.items()
        if k.startswith("init_addons_oai_record") and callable(v)
    ]
    for func in funcs:
        blueprint.record_once(func)

    return blueprint


def init_create_blueprint_from_app_oai_record(state):
    """Init app."""
    app = state.app
    ext = app.extensions["oarepo-oaipmh-record"]

    # register service
    sregistry = app.extensions["invenio-records-resources"].registry
    sregistry.register(ext.service, service_id="oarepo-oaipmh-record")

    # Register indexer
    if hasattr(ext.service, "indexer"):
        iregistry = app.extensions["invenio-indexer"].registry
        iregistry.register(ext.service.indexer, indexer_id="oarepo-oaipmh-record")


def create_blueprint_from_app_oai_recordExt(app):
    """Create -ext blueprint."""
    blueprint = Blueprint(
        "oarepo-oaipmh-record-ext", __name__, url_prefix="oarepo-oaipmh-record"
    )
    blueprint.record_once(init_create_blueprint_from_app_oai_record)

    # calls record_once for all other functions starting with "init_app_addons_"
    # https://stackoverflow.com/questions/58785162/how-can-i-call-function-with-string-value-that-equals-to-function-name
    funcs = globals()
    funcs = [
        v
        for k, v in funcs.items()
        if k.startswith("init_app_addons_oai_record") and callable(v)
    ]
    for func in funcs:
        blueprint.record_once(func)

    return blueprint

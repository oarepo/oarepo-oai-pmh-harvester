from flask import Blueprint


def create_blueprint_from_app_oai_harvester(app):
    """Create  blueprint."""
    blueprint = app.extensions["oarepo-oaipmh-harvester"].resource.as_blueprint()
    blueprint.record_once(init_create_blueprint_from_app_oai_harvester)

    # calls record_once for all other functions starting with "init_addons_"
    # https://stackoverflow.com/questions/58785162/how-can-i-call-function-with-string-value-that-equals-to-function-name
    funcs = globals()
    funcs = [
        v
        for k, v in funcs.items()
        if k.startswith("init_addons_oai_harvester") and callable(v)
    ]
    for func in funcs:
        blueprint.record_once(func)

    return blueprint


def init_create_blueprint_from_app_oai_harvester(state):
    """Init app."""
    app = state.app
    ext = app.extensions["oarepo-oaipmh-harvester"]

    # register service
    sregistry = app.extensions["invenio-records-resources"].registry
    sregistry.register(ext.service, service_id="oarepo-oaipmh-harvester")

    # Register indexer
    if hasattr(ext.service, "indexer"):
        iregistry = app.extensions["invenio-indexer"].registry
        iregistry.register(ext.service.indexer, indexer_id="oarepo-oaipmh-harvester")


def create_blueprint_from_app_oai_harvesterExt(app):
    """Create -ext blueprint."""
    blueprint = Blueprint(
        "oarepo-oaipmh-harvester-ext", __name__, url_prefix="oarepo-oaipmh-harvester"
    )
    blueprint.record_once(init_create_blueprint_from_app_oai_harvester)

    # calls record_once for all other functions starting with "init_app_addons_"
    # https://stackoverflow.com/questions/58785162/how-can-i-call-function-with-string-value-that-equals-to-function-name
    funcs = globals()
    funcs = [
        v
        for k, v in funcs.items()
        if k.startswith("init_app_addons_oai_harvester") and callable(v)
    ]
    for func in funcs:
        blueprint.record_once(func)

    return blueprint

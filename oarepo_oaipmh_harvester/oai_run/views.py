def create_api_blueprint(app):
    """Create OaiHarvesterRecord blueprint."""
    blueprint = app.extensions[
        "oarepo_oaipmh_harvester"
    ].oai_run_resource.as_blueprint()

    return blueprint

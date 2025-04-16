def create_api_blueprint(app):
    """Create OaiHarvesterRecord blueprint."""
    blueprint = app.extensions[
        "oarepo_oaipmh_harvester"
    ].oai_record_resource.as_blueprint()

    return blueprint

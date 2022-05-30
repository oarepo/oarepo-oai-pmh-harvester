def create_blueprint_from_app(app):
    """Create  blueprint."""
    return app.extensions["oaipmh_run"].resource.as_blueprint()
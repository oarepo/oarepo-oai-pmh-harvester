def create_blueprint_from_app(app):
    """Create  blueprint."""
    return app.extensions["oaipmh_record"].resource.as_blueprint()
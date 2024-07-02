def create_harvest(app):
    """Create requests blueprint."""
    ext = app.extensions["oarepo_oaipmh_harvester"]
    blueprint = ext.harvest_resource.as_blueprint()
    return blueprint

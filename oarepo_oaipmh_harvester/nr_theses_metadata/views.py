from flask import Blueprint


def create_api_blueprint(app):
    """Create  blueprint."""
    return app.extensions["nr_theses_metadata"].resource.as_blueprint()


static_blueprint = Blueprint(
    '__static_to_be_moved__',
    __name__,
    static_folder='static',
)


def create_ui_blueprint(app):
    return app.extensions["nr_theses_metadata"].ui_resource.as_blueprint()


def create_records_ui_blueprint(app):
    return app.extensions["nr_theses_metadata"].records_ui_resource.as_blueprint()

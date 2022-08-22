from . import config as config


class NrThesesMetadataExt(object):
    """extension."""

    def __init__(self, app=None):
        """Extension initialization."""
        self.resource = None
        self.ui_resource = None
        self.records_ui_resource = None
        self.service = None
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Flask application initialization."""
        self.init_config(app)
        self.init_resource(app)
        app.extensions["nr_theses_metadata"] = self

    def init_resource(self, app):
        """Initialize vocabulary resources."""
        self.service = app.config["NR_THESES_METADATA_SERVICE_CLASS"](
            config=app.config["NR_THESES_METADATA_SERVICE_CONFIG"](),
        )
        self.resource = app.config["NR_THESES_METADATA_RESOURCE_CLASS"](
            service=self.service,
            config=app.config["NR_THESES_METADATA_RESOURCE_CONFIG"](),
        )

    def init_config(self, app):
        """Initialize configuration."""
        app.config.setdefault(
            "NR_THESES_METADATA_RESOURCE_CONFIG",
            config.NR_THESES_METADATA_RESOURCE_CONFIG,
        )
        app.config.setdefault(
            "NR_THESES_METADATA_RESOURCE_CLASS",
            config.NR_THESES_METADATA_RESOURCE_CLASS,
        )

        app.config.setdefault(
            "NR_THESES_METADATA_SERVICE_CONFIG",
            config.NR_THESES_METADATA_SERVICE_CONFIG,
        )
        app.config.setdefault(
            "NR_THESES_METADATA_SERVICE_CLASS", config.NR_THESES_METADATA_SERVICE_CLASS
        )
        app.config.setdefault(
            "APP_SEARCH_FACETS", config.APP_SEARCH_FACETS
        )

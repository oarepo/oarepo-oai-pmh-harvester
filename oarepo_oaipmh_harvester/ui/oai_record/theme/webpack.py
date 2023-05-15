from invenio_assets.webpack import WebpackThemeBundle

theme = WebpackThemeBundle(
    __name__,
    "assets",
    default="semantic-ui",
    themes={
        "semantic-ui": dict(
            entry={
                "oai_record_ui_components": "./js/oai_record_ui/custom-components.js",
                "oai_record_search": "./js/oai_record_ui/search/index.js",
            },
            dependencies={},
            devDependencies={},
            aliases={},
        )
    },
)

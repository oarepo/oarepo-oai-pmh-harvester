from invenio_assets.webpack import WebpackThemeBundle

theme = WebpackThemeBundle(
    __name__,
    "assets",
    default="semantic-ui",
    themes={
        "semantic-ui": dict(
            entry={
                "oai_batch_ui_components": "./js/oai_batch_ui/custom-components.js",
                "oai_batch_search": "./js/oai_batch_ui/search/index.js",
            },
            dependencies={},
            devDependencies={},
            aliases={},
        )
    },
)

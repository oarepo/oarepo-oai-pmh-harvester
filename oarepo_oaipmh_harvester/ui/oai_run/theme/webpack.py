from invenio_assets.webpack import WebpackThemeBundle

theme = WebpackThemeBundle(
    __name__,
    "assets",
    default="semantic-ui",
    themes={
        "semantic-ui": dict(
            entry={
                "oai_run_ui_components": "./js/oai_run_ui/custom-components.js",
                "oai_run_search": "./js/oai_run_ui/search/index.js",
            },
            dependencies={},
            devDependencies={},
            aliases={},
        )
    },
)

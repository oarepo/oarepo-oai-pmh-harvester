from invenio_assets.webpack import WebpackThemeBundle

theme = WebpackThemeBundle(
    __name__,
    "assets",
    default="semantic-ui",
    themes={
        "semantic-ui": dict(
            entry={
                "oai_harvester_ui_components": "./js/oai_harvester_ui/custom-components.js",
                "oai_harvester_search": "./js/oai_harvester_ui/search/index.js",
            },
            dependencies={},
            devDependencies={},
            aliases={},
        )
    },
)

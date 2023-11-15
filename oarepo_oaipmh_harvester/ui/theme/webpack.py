from invenio_assets.webpack import WebpackThemeBundle

theme = WebpackThemeBundle(
    __name__,
    "assets",
    default="semantic-ui",
    themes={
        "semantic-ui": dict(
            entry={},
            dependencies={},
            devDependencies={},
            aliases={
                "@translations/oarepo_oaipmh_harvester": "translations/oarepo_oaipmh_harvester",
            },
        )
    },
)

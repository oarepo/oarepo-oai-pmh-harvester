import re
from io import StringIO
from typing import Union

import importlib_metadata
import yaml

from oarepo_oaipmh_harvester import cli  # noqa
from oarepo_oaipmh_harvester.harvester import harvest
from oarepo_oaipmh_harvester.oai_harvester.records.api import OaiHarvesterRecord

from . import config


class OARepoOAIHarvesterExt(object):
    """extension."""

    def __init__(self, app=None):
        """Extension initialization."""
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Flask application initialization."""
        self.app = app
        app.extensions["oarepo_oaipmh_harvester"] = self
        self.load_config(app)

    def run(
        self,
        harvester_or_code: Union[str, OaiHarvesterRecord],
        all_records=False,
        on_background=False,
        identifiers=None,
    ):
        harvest(
            harvester_or_code=harvester_or_code,
            all_records=all_records,
            on_background=on_background,
            identifiers=identifiers,
        )

    def get_parser_config(self, parser_name):
        parser_name, args = split_processor_name(parser_name)
        return {
            **(
                self.app.config["OAREPO_OAIPMH_HARVESTER_LOADERS"].get(parser_name)
                or self.app.config["DEFAULT_OAREPO_OAIPMH_HARVESTER_LOADERS"][
                    parser_name
                ]
            ),
            **args,
        }

    def get_transformer_config(self, transformer):
        transformer, args = split_processor_name(transformer)
        return {
            **(
                self.app.config["OAREPO_OAIPMH_HARVESTER_TRANSFORMERS"].get(transformer)
                or self.app.config["DEFAULT_OAREPO_OAIPMH_HARVESTER_TRANSFORMERS"][
                    transformer
                ]
            ),
            **args,
        }

    def get_writer_config(self, writer):
        writer, args = split_processor_name(writer)
        return {
            **(
                self.app.config["OAREPO_OAIPMH_HARVESTER_WRITERS"].get(writer)
                or self.app.config["DEFAULT_OAREPO_OAIPMH_HARVESTER_WRITERS"][writer]
            ),
            **args,
        }

    def load_config(self, app):
        app.config.setdefault(
            "OAREPO_OAIPMH_HARVESTER_LOADERS", config.OAREPO_OAIPMH_HARVESTER_LOADERS
        )
        app.config.setdefault("DEFAULT_OAREPO_OAIPMH_HARVESTER_LOADERS", {}).update(
            config.DEFAULT_OAREPO_OAIPMH_HARVESTER_LOADERS
        )
        app.config.setdefault(
            "OAREPO_OAIPMH_HARVESTER_TRANSFORMERS",
            config.OAREPO_OAIPMH_HARVESTER_TRANSFORMERS,
        )
        app.config.setdefault(
            "DEFAULT_OAREPO_OAIPMH_HARVESTER_TRANSFORMERS", {}
        ).update(config.DEFAULT_OAREPO_OAIPMH_HARVESTER_TRANSFORMERS)

        app.config.setdefault(
            "OAREPO_OAIPMH_HARVESTER_WRITERS",
            config.OAREPO_OAIPMH_HARVESTER_WRITERS,
        )
        app.config.setdefault("DEFAULT_OAREPO_OAIPMH_HARVESTER_WRITERS", {}).update(
            config.DEFAULT_OAREPO_OAIPMH_HARVESTER_WRITERS
        )

        app.config.setdefault("DEFAULT_DATASTREAMS_READERS", {}).update(
            config.DEFAULT_DATASTREAMS_READERS
        )

        app.config.setdefault("DEFAULT_DATASTREAMS_TRANSFORMERS", {}).update(
            config.DEFAULT_DATASTREAMS_TRANSFORMERS
        )

        app.config.setdefault("DEFAULT_DATASTREAMS_WRITERS", {}).update(
            config.DEFAULT_DATASTREAMS_WRITERS
        )

        app.config.setdefault("OAREPO_PERMISSIONS_PRESETS", {}).update(
            config.OAREPO_PERMISSIONS_PRESETS
        )

        self.set_from_entrypoints(
            "oarepo.oaipmh.loaders",
            "reader",
            app.config["DEFAULT_DATASTREAMS_READERS"],
            app.config["DEFAULT_OAREPO_OAIPMH_HARVESTER_LOADERS"],
        )

        self.set_from_entrypoints(
            "oarepo.oaipmh.transformers",
            "transformer",
            app.config["DEFAULT_DATASTREAMS_TRANSFORMERS"],
            app.config["DEFAULT_OAREPO_OAIPMH_HARVESTER_TRANSFORMERS"],
        )

        self.set_from_entrypoints(
            "oarepo.oaipmh.writers",
            "writer",
            app.config["DEFAULT_DATASTREAMS_WRITERS"],
            app.config["DEFAULT_OAREPO_OAIPMH_HARVESTER_WRITERS"],
        )

    def set_from_entrypoints(
        self, ep_group, clz_param, datastream_configs, harvester_configs
    ):
        for ep in importlib_metadata.entry_points(group=ep_group):
            cfg = ep.load()
            name = ep.name
            datastream_configs[name] = cfg["class"]
            harvester_configs[name] = {**cfg["params"], clz_param: name}


def split_processor_name(processor):
    if "{" not in processor:
        return processor, {}
    processor, rest = processor.split("{", maxsplit=1)
    rest = "{" + rest
    rest = re.sub(r"([^\\])=", r"\1: ", rest)
    rest = re.sub(r"\\(.)", r"\1", rest)
    args = yaml.safe_load(StringIO(rest))
    return processor, args

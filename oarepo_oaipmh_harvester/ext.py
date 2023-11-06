import re
from io import StringIO
from typing import Union

import importlib_metadata
import yaml

from oarepo_oaipmh_harvester import cli  # noqa
from oarepo_oaipmh_harvester.harvester import harvest
from oarepo_oaipmh_harvester.oai_harvester.records.api import OaiHarvesterRecord
from oarepo_runtime.datastreams.datastreams import Signature, SignatureKind

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

    def get_parser_signature(self, parser_name, **kwargs):
        parser_name, args = split_processor_name(parser_name)
        return Signature(
            kind=SignatureKind.READER, name=parser_name, kwargs={**args, **kwargs}
        )

    def get_transformer_signature(self, transformer, **kwargs):
        transformer, args = split_processor_name(transformer)
        return Signature(
            kind=SignatureKind.TRANSFORMER, name=transformer, kwargs={**args, **kwargs}
        )

    def get_writer_signature(self, writer, **kwargs):
        writer, args = split_processor_name(writer)
        return Signature(
            kind=SignatureKind.WRITER, name=writer, kwargs={**args, **kwargs}
        )

    def load_config(self, app):
        app.config.setdefault("DATASTREAMS_READERS", {}).update(
            config.DATASTREAMS_READERS
        )

        app.config.setdefault("DATASTREAMS_TRANSFORMERS", {}).update(
            config.DATASTREAMS_TRANSFORMERS
        )

        app.config.setdefault("DATASTREAMS_WRITERS", {}).update(
            config.DATASTREAMS_WRITERS
        )

        app.config.setdefault("OAREPO_PERMISSIONS_PRESETS", {}).update(
            config.OAREPO_PERMISSIONS_PRESETS
        )


def split_processor_name(processor):
    if "{" not in processor:
        return processor, {}
    processor, rest = processor.split("{", maxsplit=1)
    rest = "{" + rest
    rest = re.sub(r"([^\\])=", r"\1: ", rest)
    rest = re.sub(r"\\(.)", r"\1", rest)
    args = yaml.safe_load(StringIO(rest))
    return processor, args

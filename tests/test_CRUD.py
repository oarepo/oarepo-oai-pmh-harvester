import pytest

import tempfile
from flask import Flask, current_app
# from oarepo_oaipmh_harvester.oaipmh_config.proxies import current_service as config_service
from oarepo_oaipmh_harvester.oaipmh_config.ext import OaipmhConfigExt
from invenio_access.permissions import system_identity

def test_create(config_service,config_data, identity):

    item = config_service.create(identity, {'metadata': config_data})
    print(item)
    # assert item.id == lang_data["id"]
    # for k, v in lang_data.items():
    #     assert item.data[k] == v
    #
    # # Read it
    # read_item = basic_service.read(identity, ("languages", "eng"))
    #
    # assert item.id == read_item.id
    # assert item.data == read_item.data
    # assert read_item.data["type"] == "languages"
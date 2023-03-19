from flask import current_app
from werkzeug.local import LocalProxy

current_harvester = LocalProxy(
    lambda: current_app.extensions["oarepo_oaipmh_harvester"]
)

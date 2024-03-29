from flask import current_app
from werkzeug.local import LocalProxy

current_ui = LocalProxy(lambda: current_app.extensions["oai_run_ui"])
"""Proxy to the instantiated ui extension."""

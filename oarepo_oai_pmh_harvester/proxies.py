from flask import current_app
from werkzeug.local import LocalProxy

current_oai_client = LocalProxy(lambda: current_app.extensions['oarepo-oai-client'])
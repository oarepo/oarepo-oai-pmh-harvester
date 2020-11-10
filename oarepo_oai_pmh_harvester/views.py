from flask import Blueprint, abort, current_app

oai_client_blueprint = Blueprint('oai_client', __name__)


@oai_client_blueprint.route("/providers", methods=["GET"])
def get_providers():
    config = current_app.config.get("OAREPO_OAI_PROVIDERS")
    if config:
        return config
    else:
        abort(404, description="Resource not found")

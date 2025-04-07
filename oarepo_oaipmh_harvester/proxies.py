from typing import TYPE_CHECKING

from flask import current_app
from werkzeug.local import LocalProxy

if TYPE_CHECKING:
    from .ext import OARepoOAIHarvesterExt
    from .oai_run.service import OAIRunService

    current_harvester: OARepoOAIHarvesterExt
    current_oai_run_service: OAIRunService

current_harvester = LocalProxy(  # type: ignore
    lambda: current_app.extensions["oarepo_oaipmh_harvester"]
)

current_oai_run_service = LocalProxy(  # type: ignore
    lambda: current_harvester.oai_run_service
)

current_oai_record_service = LocalProxy(  # type: ignore
    lambda: current_harvester.oai_record_service
)

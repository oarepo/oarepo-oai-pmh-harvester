from datetime import datetime, timedelta

from celery import shared_task
from invenio_db import db

from ..models import OAIHarvesterRun
from ..proxies import current_oai_run_service


@shared_task
def index_oai_runs():
    """Reindex OAI data."""

    oai_runs = (
        db.session.query(OAIHarvesterRun.id)
        .filter(
            (OAIHarvesterRun.status == "running")
            | (OAIHarvesterRun.last_update_time > datetime.utcnow() - timedelta(days=1))
        )
        .yield_per(1000)
    )

    current_oai_run_service.indexer.bulk_index([u.id for u in oai_runs])

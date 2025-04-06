from datetime import datetime, timedelta

from celery import shared_task
from invenio_db import db

from ..models import OAIHarvestedRecord
from ..proxies import current_oai_record_service


@shared_task
def index_oai_records():
    """Reindex OAI data."""

    oai_records = (
        db.session.query(OAIHarvestedRecord.id)
        .filter(
            OAIHarvestedRecord.last_update_time > datetime.utcnow() - timedelta(days=1)
        )
        .yield_per(1000)
    )

    current_oai_record_service.indexer.bulk_index([u.id for u in oai_records])

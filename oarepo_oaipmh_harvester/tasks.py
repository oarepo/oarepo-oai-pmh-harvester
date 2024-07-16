from celery import shared_task

from oarepo_oaipmh_harvester.harvester import harvest


@shared_task
def harvest_task(code):
    harvest(
        harvester_or_code=code, all_records=True, on_background=True, identifiers=None
    )

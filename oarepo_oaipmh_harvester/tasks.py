from celery import shared_task

from oarepo_oaipmh_harvester.harvester import harvest


@shared_task
def harvest_task(code, manual=False, all_records=False, identifiers=None):
    harvest(
        harvester_or_code=code,
        all_records=all_records,
        manual=manual,
        identifiers=identifiers,
    )

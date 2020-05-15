import logging

from invenio_oarepo_oai_pmh_harvester.register import registry

for _ in ("elasticsearch", "urllib3"):
    logging.getLogger(_).setLevel(logging.CRITICAL)

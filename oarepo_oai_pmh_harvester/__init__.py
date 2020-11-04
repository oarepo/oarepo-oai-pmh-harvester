import logging

for _ in ("elasticsearch", "urllib3"):
    logging.getLogger(_).setLevel(logging.CRITICAL)

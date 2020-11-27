from typing import Dict

from oarepo_oai_pmh_harvester.synchronization import OAISynchronizer


class OAIProvider:
    def __init__(self, code, description: str = None,
                 synchronizers: Dict[str, OAISynchronizer] = None):
        self.code = code
        self.description = description
        self.synchronizers = synchronizers

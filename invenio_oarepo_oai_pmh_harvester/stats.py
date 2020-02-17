import json
import logging
import os
import traceback
from collections import deque
from datetime import datetime
from functools import lru_cache

import jmespath
from invenio_db import db
from sickle import Sickle

from invenio_oarepo_oai_pmh_harvester.models import OAIProvider, OAIStats
from invenio_oarepo_oai_pmh_harvester.utils import sanitize_address, add_node, update_node

log_dir = "/tmp/OAI/"

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

if not os.path.exists(log_dir):
    os.makedirs(log_dir)
log_path = os.path.join(log_dir, "stats.log")

fh = logging.FileHandler(log_path)
fh.setLevel(logging.ERROR)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(ch)


class OAIStatsRunner:
    """

    """

    def __init__(self, provider: OAIProvider, result_path=None):
        self.provider = provider
        self.sickle = Sickle(self.provider.oai_endpoint)
        self.sickle.class_mapping['ListRecords'] = self.provider.parser_instance
        self.sickle.class_mapping['GetRecord'] = self.provider.parser_instance
        self.oai_stats = None
        if result_path is not None:
            if os.path.exists(result_path):
                with open(result_path) as f:
                    self.statistics = json.load(f)
            else:
                raise FileNotFoundError(f"File: \"{result_path}\" has not been found.")
        else:
            self.statistics = {}

    def run(self):
        """

        :return:
        :rtype:
        """
        with db.session.begin_nested():
            self.oai_stats = OAIStats(provider=self.provider, stat_start=datetime.utcnow(),
                                      status="active")
            db.session.add(self.oai_stats)
        try:
            self.collect_all_unique()
            with db.session.begin_nested():
                self.oai_stats = db.session.merge(self.oai_stats)
                self.oai_stats.status = "ok"
                db.session.add(self.oai_stats)
        except:
            with db.session.begin_nested():
                self.oai_stats = db.session.merge(self.oai_stats)
                self.oai_stats.status = "failed"
                self.oai_stats.log = traceback.format_exc()
                db.session.add(self.oai_stats)
            raise
        finally:
            with db.session.begin_nested():
                self.oai_stats = db.session.merge(self.oai_stats)
                self.oai_stats.result_json = self.statistics

    def collect_all_unique(self, stat_dir="/tmp/OAI/"):
        # try:
        records = self.sickle.ListRecords(metadataPrefix=self.provider.metadata_prefix)
        for num, record in enumerate(records):
            try:
                logger.info(f"{num}. Record: {record.header.identifier}")
                for address in record.record_map.keys():
                    address_list = address.split(".")
                    address_queue = deque(address_list)
                    source = self._search_address(address)
                    if source is None:
                        self._insert_value(address_queue, {}, self.statistics)
                    else:
                        if address in record.field_map:
                            fields = record.get_field(address)
                            address = add_node(address, "field")
                            address_list = address.split(".")
                            source = self._search_address(address)
                            if source is None:
                                self._insert_value(deque(address_list), set(), self.statistics)
                            else:
                                self.statistics = update_node(address, self.statistics, fields)
            except Exception as e:
                logger.error(str(e))
        # finally:
        #     if not os.path.exists(stat_dir):
        #         os.makedirs(stat_dir)
        #     stat_path = os.path.join(log_dir, "stats.json")
        #     with open(stat_path, "w") as fp:
        #         json.dump(self.statistics, fp, ensure_ascii=False, indent=4, cls=SetEncoder)

    @lru_cache(100)
    def _search_address(self, address):
        """

        :param address:
        :type address:
        :return:
        :rtype:
        """
        source = jmespath.search(sanitize_address(address), self.statistics)
        return source

    def _insert_value(self, address_queue, value, node):
        """

        :param node:
        :type node:
        :param address_queue:
        :type address_queue:
        :param value:
        :type value:
        :return:
        :rtype:
        """
        while len(address_queue) > 0:
            k = address_queue.popleft()
            node = node.setdefault(k, value)
        return node

    # TODO: dopsat metodu na zpracování hrubých dat
    def process_data(self):
        pass

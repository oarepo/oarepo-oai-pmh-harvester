from collections import deque

import jmespath
from sickle import Sickle

from invenio_oarepo_oai_pmh_harvester.models import OAIProvider
from invenio_oarepo_oai_pmh_harvester.utils import sanitize_address, add_node, update_node


class OAIStats:
    """

    """

    def __init__(self, provider: OAIProvider):
        self.provider = provider
        self.sickle = Sickle(self.provider.oai_endpoint)
        self.sickle.class_mapping['ListRecords'] = self.provider.parser_instance
        self.sickle.class_mapping['GetRecord'] = self.provider.parser_instance
        self.statistics = {}

    # TODO: catch errors and save it into log file.
    def run(self):
        records = self.sickle.ListRecords(metadataPrefix=self.provider.metadata_prefix)
        for num, record in enumerate(records):
            print(f"{num}.", "Record:", record.header.identifier)
            for address in record.record_map.keys():
                address_list = address.split(".")
                address_queue = deque(address_list)
                source = jmespath.search(sanitize_address(address), self.statistics)
                if source is None:
                    self.insert_value(address_queue, {}, self.statistics)
                else:
                    if address in record.field_map:
                        fields = record.get_field(address)
                        address = add_node(address, "field")
                        address_list = address.split(".")
                        source = jmespath.search(sanitize_address(address),
                                                 self.statistics)
                        if source is None:
                            self.insert_value(deque(address_list), set(), self.statistics)
                        else:
                            self.statistics = update_node(address, self.statistics, fields)
            print(self.statistics)

    def insert_value(self, addres_queue, value, node):
        """

        :param node:
        :type node:
        :param addres_queue:
        :type addres_queue:
        :param value:
        :type value:
        :return:
        :rtype:
        """
        while len(addres_queue) > 0:
            k = addres_queue.popleft()
            node = node.setdefault(k, value)
        return node


class Element:
    """

    """

    def __init__(self, name):
        self.name = name

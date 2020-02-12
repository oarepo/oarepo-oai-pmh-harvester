from collections import deque

import jmespath


# TODO: přesunout do JMESPath a udělat PR
def sanitize_address(address: str):
    """

    :param address:
    :type address:
    :return:
    :rtype:
    """
    address_list = address.split(".")
    address_list = ["\"" + addr + "\"" for addr in address_list]
    return ".".join(address_list)


# TODO: přesunout do JMESPath a udělat PR
def add_node(address: str, node: str):
    """

    :param node:
    :type node:
    :param address:
    :type address:
    :return:
    :rtype:
    """
    return f"{address}.{node}"


# TODO: přesunout do JMESPath a udělat PR
def update_node(address, tree, value):
    """

    :param value:
    :type value:
    :param address:
    :type address:
    :param tree:
    :type tree:
    :return:
    :rtype:
    """
    address_list = address.split(".")
    old_value = jmespath.search(sanitize_address(".".join(address_list)), tree)
    new_value = old_value.copy()
    new_value.update(value)
    k = address_list.pop()
    while len(address_list) > 0:
        old_value = jmespath.search(sanitize_address(".".join(address_list)), tree)
        old_value[k] = new_value
        new_value = old_value
        k = address_list.pop()
    tree[k] = old_value
    return tree

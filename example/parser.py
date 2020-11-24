from collections import defaultdict

from oarepo_oai_pmh_harvester.decorators import parser


def xml_to_dict_xoai(tree):
    tree_dict = defaultdict(list)
    children = list(tree)
    if len(children) == 0:
        return tree.text
    for child in children:
        name = child.get("name")
        tree_dict[name].append(xml_to_dict_xoai(child))
    remove_key(tree_dict, "none")
    remove_key(tree_dict, "null")
    remove_key(tree_dict, None)
    tree_dict.pop("none", True)
    tree_dict.pop("null", True)
    tree_dict.pop(None, True)
    return tree_dict


@parser("xoai")
def xoai_parser_refine(etree):
    return xml_to_dict_xoai(list(list(etree)[1])[0])


def remove_key(tree_dict, key):
    if key in tree_dict:
        for item in tree_dict[key]:
            for k, v in item.items():
                tree_dict[k].append(v)

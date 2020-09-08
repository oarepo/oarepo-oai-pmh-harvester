from collections import defaultdict


def infinite_dd():
    return defaultdict(infinite_dd)

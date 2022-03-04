from collections import defaultdict

from dojson.contrib.marc21.utils import create_record, GroupableOrderedDict

from oarepo_oaipmh_harvester.models import OAIHarvesterConfig


class IdentityParser:
    def __init__(self, harvester: OAIHarvesterConfig):
        pass

    def parse(self, record):
        return record


class OAIParser:
    def __init__(self, harvester: OAIHarvesterConfig):
        self.harvester = harvester

    def parse(self, oai_record):
        return {
            'datestamp': oai_record.header.datestamp,
            'deleted': oai_record.header.deleted,
            'identifier': oai_record.header.identifier,
            'metadata': self.parse_metadata(oai_record),
        }

    def parse_metadata(self, oai_record):
        return None


class MarcxmlParser(OAIParser):

    def parse_metadata(self, oai_record):
        ret = {}
        for k, vals in create_record(oai_record.xml).items():
            if k == '__order__':
                continue
            if isinstance(vals, GroupableOrderedDict):
                for kk, v in vals.items():
                    if kk == '__order__':
                        continue
                    ret[k + kk] = v
            elif isinstance(vals, tuple):
                lret = defaultdict(list)
                for idx, vval in enumerate(vals):
                    for kk, v in vval.items():
                        if kk == '__order__':
                            continue
                        if (k + kk) not in lret and idx:
                            lret[k + kk] = [None] * idx
                        lret[k + kk].append(v)
                    for v in lret.values():
                        if len(v) <= idx:
                            v.append(None)

                ret.update({
                    k: tuple(v) for k, v in lret.items()
                })
            else:
                ret[k] = vals
        return ret

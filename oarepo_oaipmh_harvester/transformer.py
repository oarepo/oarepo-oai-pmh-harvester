import functools
import itertools
import traceback
from typing import List, Any, Dict

from oarepo_oaipmh_harvester.models import OAIHarvesterConfig, OAIHarvestRun, OAIHarvestRunBatch
from invenio_access.permissions import system_identity


class OAIRecord:
    def __init__(self, record, current=None, prefix=None):
        self._data = current or record['metadata']
        self._prefix = prefix + "." if prefix else ""
        self._record = record
        self._transformed = {}
        self._model = None
        self._service = None
        if not current:
            self._record['processed'] = {'leader'}

    def __getitem__(self, key):
        if key in self._data:
            self._record['processed'].add(self._prefix + key)
            return self._data[key]
        raise KeyError(f"Key {key} not in record's metadata {'at path ' + self._prefix if self._prefix else ''}")

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def ignore(self, key):
        self.get(key)

    def __contains__(self, key):
        return key in self._data

    @property
    def unprocessed(self):
        ret = []
        for k in self._data:
            if k not in self._record['processed']:
                ret.append(k)
        return list(sorted(ret))

    @property
    def transformed(self):
        return self._transformed

    @property
    def identifier(self):
        return self._record['identifier']

    @property
    def datestamp(self):
        return self._record['datestamp']

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, value):
        self._model = value

    @property
    def service(self):
        return self._service

    @service.setter
    def service(self, value):
        self._service = value


class OAITransformer:
    @property
    def oaiidentifier_search_property(self):
        raise NotImplementedError(
            'Add oaiidentifier_search_property property with the name of the filter for oai identifier')

    @property
    def oaiidentifier_search_path(self):
        raise NotImplementedError(
            'Add oaiidentifier_search_path property returning tuple of path within the record to oai identifier')

    @property
    def record_service(self):
        raise NotImplementedError(
            'Add record_service property returning the service to be used for creating/updating/deleting records')

    @property
    def record_model(self):
        raise NotImplementedError(
            'Add record_model property returning the record class')

    def __init__(self, harvester_config: OAIHarvesterConfig, harvester_run: OAIHarvestRun):
        self.harvester_config = harvester_config
        self.harvest_run = harvester_run

    def transform(self, oai_records: List[OAIRecord], harvest_batch: OAIHarvestRunBatch):
        """
        Transforms records from oai_record["..."] into oai_record.transformed and fills in
        oai_record.service and oai_record.model

        :param oai_records:         a list of oai-pmh records
        :param harvest_batch:       a harvester batch, for example for reporting errors etc.
        """
        for rec in oai_records:
            try:
                self.transform_single(rec)
            except Exception as e:
                harvest_batch.record_exception(rec.identifier, e)
                continue

            rec.service = self.get_record_service(rec)
            rec.model = self.get_record_model(rec)

    def transform_deleted(self, oai_records: List[OAIRecord], harvest_batch: OAIHarvestRunBatch):
        """
        Fills in oai_record.service and oai_record.model

        :param oai_records:         a list of oai-pmh records
        :param harvest_batch:       a harvester batch, for example for reporting errors etc.
        """
        for rec in oai_records:
            rec.service = self.get_record_service(rec)
            rec.model = self.get_record_model(rec)

    def get_record_service(self, rec: OAIRecord):
        return self.record_service

    def get_record_model(self, rec: OAIRecord):
        return self.record_model

    def transform_single(self, rec: OAIRecord):
        raise NotImplementedError()

    def save(self, oai_records: List[OAIRecord], harvest_batch: OAIHarvestRunBatch, uow):
        services = {}
        for rec in oai_records:
            sid = id(rec.service)
            if sid not in services:
                services[sid] = (rec.service, [])
            services[sid][1].append(rec)

        for service, records_to_save in services.values():
            try:
                found, extra = self.categorize(service, records_to_save)
                # save found only if differ
                if found:
                    for r, found_id in found:
                        try:
                            service.update(system_identity, found_id, r.transformed, uow=uow)
                        except Exception as e:
                            traceback.print_exc()
                            harvest_batch.record_exception(r.identifier, e, record=r)
                # save extra always
                for r in extra:
                    try:
                        service.create(system_identity, r.transformed, uow=uow)
                    except Exception as e:
                        traceback.print_exc()
                        harvest_batch.record_exception(r.identifier, e, record=r)
            except Exception as e:
                traceback.print_exc()
                for r in records_to_save:
                    harvest_batch.record_exception(r.identifier, e, record=r)

    def delete(self, oai_records: List[OAIRecord], harvest_batch: OAIHarvestRunBatch, uow):
        services = {}
        for rec in oai_records:
            sid = id(rec.service)
            if sid not in services:
                services[sid] = (rec.service, [])
            services[sid][1].append(rec)

        for service, records_to_delete in services.values():
            try:
                found, __ = self.categorize(service, records_to_delete)
                # save found only if differ
                for r, found_id in found:
                    try:
                        service.delete(system_identity, found_id, uow=uow)
                    except Exception as e:
                        traceback.print_exc()
                        harvest_batch.record_exception(r.identifier, e, record=r)
            except Exception as e:
                traceback.print_exc()
                for r in records_to_delete:
                    harvest_batch.record_exception(r.identifier, e, record=r)

    def categorize(self, service, records):
        found_items = service.search(system_identity, params={
            'facets': {
                self.oaiidentifier_search_property: [x.identifier for x in records]
            },
            'size': len(records) + 1
        })
        hits = list(found_items.hits)
        found = []
        extra = []
        cache = {}
        for r in records:
            found_identifier = self.find_in_resultset(r, hits, cache)
            if found_identifier:
                found.append((r, found_identifier))
            else:
                extra.append(r)
        return found, extra

    def find_in_resultset(self, rec, resultset, cache):
        if 'by_identifier' not in cache:
            by_identifier = {}

            def find_identifiers(x, path):
                if not path:
                    yield x
                else:
                    if isinstance(x, list):
                        for y in x:
                            yield from find_identifiers(y, path)
                    elif isinstance(x, dict):
                        if path[0] in x:
                            yield from find_identifiers(x[path[0]], path[1:])

            for r in resultset:
                for ident in find_identifiers(r, self.oaiidentifier_search_path):
                    by_identifier[ident] = r
            cache['by_identifier'] = by_identifier
        found_record = cache['by_identifier'].get(rec.identifier)
        if found_record:
            return found_record['id']
        return None


def matches(*args, first_only=False, paired=False, unique=False):
    def wrapper(f):
        @functools.wraps(f)
        def wrapped(md, rec):
            if paired:
                vals = []
                for arg in args:
                    if arg not in rec:
                        return
                    vals.append(rec[arg])
                if isinstance(vals[0], (tuple, list)):
                    # zip longest
                    items = set()
                    for v in itertools.zip_longest(*vals):
                        if not unique or tuple(v) not in items:
                            f(md, rec, v)
                            items.add(tuple(v))
                else:
                    f(md, rec, vals)
                return

            items = set()
            for arg in args:
                if arg in rec:
                    val = rec[arg]
                    if isinstance(val, (list, tuple)):
                        for vv in val:
                            if not unique or vv not in items:
                                f(md, rec, vv)
                                items.add(vv)
                    else:
                        if not unique or val not in items:
                            f(md, rec, val)
                            items.add(val)
                    if first_only:
                        break

        return wrapped

    return wrapper


def make_array(*vals_and_conditions):
    """
    make array from list of [condition, value, condition, value, ...]
    If condition is true, add value to the resulting list, otherwise silently drop
    condition and value might be callables
    """
    ret = []
    for i in range(0, len(vals_and_conditions), 2):
        cond = vals_and_conditions[i]
        if callable(cond):
            cond = cond()
        if not cond:
            continue
        val = vals_and_conditions[i + 1]
        if callable(val):
            val = val()
        ret.append(val)
    return ret


def make_dict(*pairs):
    ret = {}
    for i in range(0, len(pairs), 2):
        k = pairs[i]
        v = pairs[i + 1]
        if v:
            ret[k] = v
    return ret

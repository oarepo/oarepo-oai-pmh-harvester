import functools
import itertools
import json
from abc import abstractmethod
from collections import defaultdict
from typing import List
import traceback

from oarepo_runtime.datastreams import StreamEntry
from oarepo_runtime.datastreams.transformers import BatchTransformer, StreamBatch
from oarepo_runtime.datastreams.errors import TransformerError


class OAIRuleTransformer(BatchTransformer):
    def __init__(self, identity, **kwargs) -> None:
        super().__init__()
        self.late_actions = defaultdict(list)
        self.identity = identity

    def apply_batch(self, batch: StreamBatch, *args, **kwargs) -> List[StreamEntry]:
        if not len(batch.entries):
            return batch
        for entry in batch.entries:
            entry.transformed = {}
            entry.processed = set()
            try:
                self.transform(entry)
            except TransformerError as e:
                stack = "\n".join(traceback.format_stack())
                entry.errors.append(f"Transformer error: {e}: {stack}")
            except Exception as e:
                stack = "\n".join(traceback.format_stack())
                entry.errors.append(f"Transformer unhandled error: {e}: {stack}")

        self.finish_transformation(batch.entries)
        return batch

    @abstractmethod
    def transform(self, entry: StreamEntry):
        """Please add your code here"""

    def register_late_action(self, action_name, entry, **action_params):
        self.late_actions[action_name].append((entry, action_params))

    def finish_transformation(self, entries: List[StreamEntry]):
        for k, v in self.late_actions:
            getattr(self, k)(v)
        for entry in entries:
            entry.entry = entry.transformed
            delattr(entry, "transformed")
            delattr(entry, "processed")


def matches(*args, first_only=False, paired=False, unique=False):
    def wrapper(f):
        @functools.wraps(f)
        def wrapped(md, entry):
            entry.processed.update(args)
            untransformed_data = entry.entry
            if paired:
                vals = []
                for arg in args:
                    val = untransformed_data.get(arg)
                    if val is None:
                        val = []
                    elif not isinstance(val, (list, tuple)):
                        val = [val]
                    vals.append(val)

                # zip longest
                items = set()
                for v in itertools.zip_longest(*vals):
                    if not unique or tuple(v) not in items:
                        f(md, entry, v)
                        items.add(tuple(v))
                return

            items = set()
            for arg in args:
                if arg in untransformed_data:
                    val = untransformed_data[arg]
                    if isinstance(val, (list, tuple)):
                        for vv in val:
                            if not unique or vv not in items:
                                f(md, entry, vv)
                                items.add(vv)
                    else:
                        if not unique or val not in items:
                            f(md, entry, val)
                            items.add(val)
                    if first_only:
                        break

        return wrapped

    return wrapper


def deduplicate(md, what):
    contribs = [json.dumps(x, sort_keys=True) for x in md.get(what, [])]
    for idx in range(len(contribs) - 1, -1, -1):
        for pidx in range(0, idx):
            if contribs[idx] == contribs[pidx]:
                del contribs[idx]
                del md[what][idx]
                break


def ignore(entry, *args):
    entry.processed.update(args)


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

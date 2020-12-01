import traceback

from oarepo_oai_pmh_harvester.utils import merge


class OAITransformer:
    PHASE_PRE = "pre"
    PHASE_POST = "post"
    PROCESSED = "ok"
    NO_HANDLER_CALLED = "no_handler_called"

    def __init__(self, rules: dict = None, unhandled_paths: set = None, **options):
        if rules is None:
            rules = {}
        if unhandled_paths is None:
            unhandled_paths = set()
        self.rules = rules
        self.options = options
        self.unhandled_paths = unhandled_paths

    def transform(self, record):
        result = {}
        if self.iter_json(el=record, paths=[""], results=[result],
                          record=record) is not OAITransformer.PROCESSED:
            raise Exception("Top level handler returned unexpected result")  # pragma: no cover
        return result

    def iter_json(self, el, paths, results, record=None):
        """

        """
        # print(" " * 4 * len(paths), f"Iter element {repr(el)[:100]}")
        # List items call themselves
        if isinstance(el, (list, tuple)):
            result = self.call_handlers(paths=paths, el=el, results=results,
                                        phase=OAITransformer.PHASE_PRE, record=record)
            if result == OAITransformer.PROCESSED:
                return result
            for _ in el:
                if self.iter_json(_, paths, results, record=record) is not OAITransformer.PROCESSED:
                    raise ValueError(  # pragma: no cover
                        f"Path {paths} has not been processed by any handler {_}")
            result = self.call_handlers(paths=paths, el=el, results=results,
                                        phase=OAITransformer.PHASE_POST, record=record)
            if result is OAITransformer.NO_HANDLER_CALLED:
                return OAITransformer.PROCESSED
            return result

        # Dict
        elif isinstance(el, dict):
            result = self.call_handlers(paths=paths, el=el, results=results,
                                        phase=OAITransformer.PHASE_PRE, record=record)
            if result == OAITransformer.PROCESSED:
                return result
            for k, v in el.items():
                child_paths = [*(f"{path}/{k}" for path in paths), k]
                if result != OAITransformer.NO_HANDLER_CALLED:
                    child_results = [*results, result]
                else:
                    child_results = results
                if self.iter_json(v, child_paths,
                                  child_results, record=record) is not OAITransformer.PROCESSED:
                    raise ValueError(
                        f"Path {child_paths} has not been processed by any handler {v}")
            result = self.call_handlers(paths=paths, el=el, results=results,
                                        phase=OAITransformer.PHASE_POST, record=record)
            if result is OAITransformer.NO_HANDLER_CALLED:
                return OAITransformer.PROCESSED
            return result

        # string
        elif isinstance(el, (str, int, float)):
            result = self.call_handlers(paths=paths, el=el, results=results,
                                        phase=OAITransformer.PHASE_PRE, record=record)
            if result == OAITransformer.PROCESSED:
                return result
            else:
                raise ValueError(f"Path {paths} has not been processed by any handler {el}")
        else:
            raise ValueError(
                f"Path with simple value {paths} has not been processed by any handler {el}")

    def call_handlers(self, paths, el, results, phase, record=None, **kwargs):
        paths = set(paths)
        intersec = paths.intersection(self.unhandled_paths)
        if intersec:
            return OAITransformer.PROCESSED
        for path in paths:
            if path not in self.rules:
                continue
            handler = self.rules[path]
            if phase not in handler:
                continue
            try:
                ret = handler[phase](el=el, paths=paths, results=results, phase=phase,
                                     record=record,
                                     **self.options)
            except Exception:
                exc = traceback.format_exc()
                if not "rulesExceptions" in results[-1]:
                    results[-1]["rulesExceptions"] = []
                results[-1]["rulesExceptions"].append(
                    {"path": path, "element": el, "phase": phase, "exception": exc})
                return OAITransformer.PROCESSED
            assert ret is not None, f"Handler {handler[phase]} must not return None"
            if isinstance(ret, dict):
                results[-1] = merge(results[-1], ret)
                ret = OAITransformer.PROCESSED
            elif ret == OAITransformer.PROCESSED:
                pass
            else:
                raise Exception(f"Rule must return dictionary, {type(ret)} have been returned")
            return ret
        return OAITransformer.NO_HANDLER_CALLED

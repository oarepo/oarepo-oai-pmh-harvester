import traceback

from oarepo_oai_pmh_harvester.decorators import rule_error_handler


@rule_error_handler("uk", "xoai")
def error_handler_1(el, path, phase, results):
    exc = traceback.format_exc()
    if not "rulesExceptions" in results[-1]:
        results[-1]["rulesExceptions"] = []
    results[-1]["rulesExceptions"].append(
        {"path": path, "element": el, "phase": phase, "exception": exc})

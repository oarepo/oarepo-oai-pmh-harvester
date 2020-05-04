# import functools
# import inspect
#
# from invenio_oarepo_oai_pmh_harvester.transformer import OAITransformer
#
#
# def pre_rule(path):
#     def wrapper(func):
#         func._transform_path = path
#         func._transform_phase = OAITransformer.PHASE_PRE
#         return func
#
#     return wrapper
#
#
# def post_rule(path):
#     def wrapper(func):
#         func._transform_path = path
#         func._transform_phase = OAITransformer.PHASE_POST
#         return func
#
#     return wrapper
#
#
# def array_value(func):
#     @functools.wraps(func)
#     def wrapped(**kwargs):
#         ret = func(**kwargs)
#         if isinstance(ret, list):
#             kwargs["results"][-1].extend(ret)
#         else:
#             kwargs["results"][-1].append(ret)
#         return OAITransformer.PROCESSED
#
#     return wrapped
#
#
# # TODO: přesunot do registrů
# class Rules:
#     def __init__(self):
#         self.rules = {}
#         for name, method in inspect.getmembers(self, inspect.ismethod):
#             if not hasattr(method, "_transform_path"):
#                 continue
#             _transform_path = method._transform_path
#             _transform_phase = method._transform_phase
#             if _transform_path not in self.rules:
#                 self.rules[_transform_path] = {}
#             self.rules[_transform_path][_transform_phase] = method

# import logging
#
# import click
# from flask import cli, current_app
# from invenio_db import db
# from invenio_nusl.cli import nusl
# from invenio_nusl_theses.proxies import nusl_theses
# from oarepo_oai_pmh_harvester.models import OAIProvider
# from oarepo_oai_pmh_harvester.synchronization import OAISynchronizer
#
#
# @nusl.group()
# def oai():
#     pass
#
#
# @oai.group()
# def synchronize():
#     pass
#
#
# @synchronize.command("uk")
# @click.option('-s', '--start', default=0)
# @click.option('-o', '--start-oai')
# @click.option('--break-on-error/--no-break-on-error', default=True)
# @cli.with_appcontext
# def import_uk(start, start_oai, break_on_error):
#     for _ in ("elasticsearch", "urllib3"):
#         logging.getLogger(_).setLevel(logging.CRITICAL)
#     uk_provider = OAIProvider.query.filter_by(code="uk").one_or_none()
#     SERVER_NAME = current_app.config["SERVER_NAME"]
#     print("SERVER_NAME", SERVER_NAME)
#     constant_fields = {
#         "provider": {"$ref": f"http://{SERVER_NAME}/api/taxonomies/institutions/00216208/"},
#         "accessRights": {"$ref": f"http://{SERVER_NAME}/api/taxonomies/accessRights/c_abf2/"},
#         "accessibility": [{"lang": "cze", "value": "Dostupné v digitálním repozitáři UK."}, {
#             "lang": "eng", "value": "Available in the Charles University Digital Repository."
#         }]
#     }
#     if not uk_provider:
#         uk_provider = OAIProvider(
#             code="uk",
#             description="Univerzita Karlova",
#             oai_endpoint="https://dspace.cuni.cz/oai/nusl",
#             set_="nusl_set",
#             metadata_prefix="xoai",
#             constant_fields=constant_fields
#         )
#         db.session.add(uk_provider)
#         db.session.commit()
#     unhandled_paths = {
#         "/dc/date/accessioned",
#         "/dc/date/available",
#         "/dc/date/issued",
#         "/dc/identifier/repId",
#         "/dc/identifier/aleph",
#         "/dc/description/provenance",
#         "/dc/description/department",
#         "/dc/description/faculty",
#         "/dc/language/cs_CZ",
#         "/dc/publisher",
#         "/dcterms/created",
#         "/thesis/degree/name",
#         "/thesis/degree/program",
#         "/thesis/degree/level",
#         "/uk/abstract",
#         "/uk/thesis",
#         "/uk/taxonomy",
#         "/uk/faculty-name",
#         "/uk/faculty-abbr",
#         "/uk/file-availability",
#         "/uk/degree-discipline",
#         "/uk/degree-program",
#         "/uk/publication-place",
#         "/bundles",
#         "/others/handle",
#         "/others/lastModifyDate",
#         "/repository"
#     }
#     sync = OAISynchronizer(
#         uk_provider,
#         parser_name="xoai",
#         unhandled_paths=unhandled_paths,
#         create_record=nusl_theses.create_draft_record,
#         update_record=nusl_theses.update_draft_record,
#         delete_record=nusl_theses.delete_draft_record,
#         pid_type="dnusl",
#         validation=nusl_theses.validate
#     )
#     api = current_app.wsgi_app.mounts['/api']
#     with api.app_context():
#         sync.run(start_id=start, start_oai=start_oai, break_on_error=break_on_error)

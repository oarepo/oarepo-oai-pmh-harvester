from invenio_nusl_theses.proxies import nusl_theses

from invenio_oarepo_oai_pmh_harvester.models import OAIProvider
from invenio_db import db

from invenio_oarepo_oai_pmh_harvester.synchronization import OAISynchronizer


def test_uk_one_record(app, uk_db, schemas):
    uk_provider = OAIProvider.query.filter_by(code="uk").one_or_none()
    constant_fields = {
        "provider": {"$ref": "http://127.0.0.1:5000/api/taxonomies/institutions/00216208/"},
        "accessRights": {"$ref": "http://127.0.0.1:5000/api/taxonomies/accessRights/c_abf2/"},
        "accessibility": [{"lang": "cze", "value": "Dostupné v digitálním repozitáři UK."}, {
            "lang": "eng", "value": "Available in the Charles University Digital Repository."
        }]
    }
    if not uk_provider:
        uk_provider = OAIProvider(
            code="uk",
            description="Univerzita Karlova",
            oai_endpoint="https://dspace.cuni.cz/oai/nusl",
            set_="nusl_set",
            metadata_prefix="xoai",
            constant_fields=constant_fields
        )
        db.session.add(uk_provider)
        db.session.commit()
    unhandled_paths = {
        "/dc/date/accessioned",
        "/dc/date/available",
        "/dc/date/issued",
        "/dc/identifier/repId",
        "/dc/identifier/aleph",
        "/dc/description/provenance",
        "/dc/description/department",
        "/dc/description/faculty",
        "/dc/language/cs_CZ",
        "/dc/publisher",
        "/dcterms/created",
        "/thesis/degree/name",
        "/thesis/degree/program",
        "/thesis/degree/level",
        "/uk/abstract",
        "/uk/thesis",
        "/uk/taxonomy",
        "/uk/faculty-name",
        "/uk/faculty-abbr",
        "/uk/degree-discipline",
        "/uk/degree-program",
        "/uk/publication-place",
        "uk/file-availability",
        "/bundles",
        "/others/handle",
        "/others/lastModifyDate",
        "/repository"
    }
    sync = OAISynchronizer(
        uk_provider,
        parser_name="xoai",
        unhandled_paths=unhandled_paths,
        create_record=nusl_theses.create_draft_record,
        update_record=nusl_theses.update_draft_record,
        delete_record=nusl_theses.delete_draft_record,
        pid_type="dnusl",
        validation=nusl_theses.validate,
        oai_identifiers=["oai:dspace.cuni.cz:20.500.11956/111006"]
    )
    sync.run()


def test_transformer_uk_sample(app, uk_db, schemas):
    uk_provider = OAIProvider.query.filter_by(code="uk").one_or_none()
    constant_fields = {
        "provider": {"$ref": "http://127.0.0.1:5000/api/taxonomies/institutions/00216208/"},
        "accessRights": {"$ref": "http://127.0.0.1:5000/api/taxonomies/accessRights/c_abf2/"},
        "accessibility": [{"lang": "cze", "value": "Dostupné v digitálním repozitáři UK."}, {
            "lang": "eng", "value": "Available in the Charles University Digital Repository."
        }]
    }
    if not uk_provider:
        uk_provider = OAIProvider(
            code="uk",
            description="Univerzita Karlova",
            oai_endpoint="https://dspace.cuni.cz/oai/nusl",
            set_="nusl_set",
            metadata_prefix="xoai",
            constant_fields=constant_fields
        )
        db.session.add(uk_provider)
        db.session.commit()
    unhandled_paths = {
        "/dc/date/accessioned",
        "/dc/date/available",
        "/dc/date/issued",
        "/dc/identifier/repId",
        "/dc/identifier/aleph",
        "/dc/description/provenance",
        "/dc/description/department",
        "/dc/description/faculty",
        "/dc/language/cs_CZ",
        "/dc/publisher",
        "/dcterms/created",
        "/thesis/degree/name",
        "/thesis/degree/program",
        "/thesis/degree/level",
        "/uk/abstract",
        "/uk/thesis",
        "/uk/taxonomy",
        "/uk/faculty-name",
        "/uk/faculty-abbr",
        "/uk/degree-discipline",
        "/uk/degree-program",
        "/uk/publication-place",
        "uk/file-availability",
        "/bundles",
        "/others/handle",
        "/others/lastModifyDate",
        "/repository"
    }
    sync = OAISynchronizer(
        uk_provider,
        parser_name="xoai",
        unhandled_paths=unhandled_paths,
        create_record=nusl_theses.create_draft_record,
        update_record=nusl_theses.update_draft_record,
        delete_record=nusl_theses.delete_draft_record,
        pid_type="dnusl",
        validation=nusl_theses.validate,
        oai_identifiers=["oai:dspace.cuni.cz:20.500.11956/4434"]
    )
    sync.run()

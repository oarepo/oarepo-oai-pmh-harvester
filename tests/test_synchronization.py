import pytest

from invenio_oarepo_oai_pmh_harvester.models import OAIProvider
from invenio_db import db

from invenio_oarepo_oai_pmh_harvester.synchronization import OAISynchronizer


def test_synchronization_instance(app, db, unhandled_paths):
    provider = OAIProvider.query.filter_by(code="uk").one_or_none()
    if not provider:
        provider = OAIProvider(
            code="uk",
            oai_endpoint="https://dspace.cuni.cz/oai/nusl",
            set_="nusl_set",
            metadata_prefix="xoai"
        )
        db.session.add(provider)
        db.session.commit()
    synchronizer = OAISynchronizer(provider, 'xoai', unhandled_paths=unhandled_paths)
    print(synchronizer)
    synchronizer.run()


@pytest.fixture()
def unhandled_paths():
    return {
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
        "/bundles",
        "/others/handle",
        "/others/lastModifyDate",
        "/repository"
    }

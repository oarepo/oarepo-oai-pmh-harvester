from invenio_app.factory import create_app

from oarepo_oaipmh_harvester.cli import _add_harvester
from oarepo_oaipmh_harvester.harvester import harvest


def run():
    harvester = _add_harvester(
        code="nusl",
        name="NUŠL",
        url="http://invenio.nusl.cz/oai2d/",
        set="global",
        prefix="marcxml",
        loader="sickle",
        transformers=["marcxml"],
        comment="NUSL loader",
        max_records=None,
        batch_size=100,
        writer="oai_dir",
        writer_params=[{"param": "dir", "value": "../oai-data"}],
    )
    harvest(harvester_or_code="nusl", all_records=True, on_background=False)


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        run()

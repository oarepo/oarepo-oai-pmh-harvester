from invenio_oarepo_oai_pmh_harvester.migration import OAIMigration


def test_migrate(app, db):
    def oai_id_handler(json):
        identifiers = json["identifier"]
        return \
        [identifier["value"] for identifier in identifiers if identifier["type"] == "nuslOAI"][0]

    migrator = OAIMigration(handler=oai_id_handler)
    migrator.migrate()

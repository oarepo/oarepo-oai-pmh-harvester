from oarepo_oai_pmh_harvester.migration import OAIMigration
from oarepo_oai_pmh_harvester.models import OAIRecord


def test_migrate(app, test_db, sample_record, migrate_provider):
    def oai_id_handler(json):
        identifiers = json["identifier"]
        return \
            [identifier["value"] for identifier in identifiers if
             identifier["type"] == "originalOAI"][0]

    migrator = OAIMigration(handler=oai_id_handler, provider=migrate_provider)
    migrator.run()
    result = OAIRecord.query.filter_by(oai_identifier='oai:server:id').one_or_none()
    assert result is not None


def test_migrate_2(app, test_db, sample_record, migrate_provider):
    def oai_id_handler(json):
        pass

    migrator = OAIMigration(handler=oai_id_handler, provider=migrate_provider)
    migrator.run()
    result = OAIRecord.query.filter_by(oai_identifier='oai:server:id').one_or_none()
    assert result is None

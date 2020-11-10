from oarepo_oai_pmh_harvester.models import OAIRecord, OAISync
from oarepo_oai_pmh_harvester.proxies import current_oai_client


def test_get_record(load_entry_points, app, db, record_xml):
    synchronizer = current_oai_client.providers["uk"].synchronizers["xoai"]
    oai_sync = OAISync(provider_code="uk")
    synchronizer.oai_sync = oai_sync
    record = synchronizer.create_or_update("oai:dspace.cuni.cz:20.500.11956/2623",
                                           '2017-09-11T08:12:53Z', xml=record_xml)
    db.session.commit()
    assert record == {'pid': '1', 'title': 'Testovací záznam'}
    oai_rec = OAIRecord.get_record("oai:dspace.cuni.cz:20.500.11956/2623")
    assert oai_rec is not None
    assert isinstance(oai_rec, OAIRecord)

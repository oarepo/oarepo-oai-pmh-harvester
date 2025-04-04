from pathlib import Path
from pprint import pprint

from invenio_access.permissions import system_identity

from oarepo_oaipmh_harvester.cli import _add_harvester
from oarepo_oaipmh_harvester.harvester import harvest
from oarepo_oaipmh_harvester.models import OAIHarvestedRecord, OAIHarvesterRun


def test_harvest_synchronous(
    app, db, client, search_clear, default_community, mappings
):
    import logging

    logging.basicConfig(level=logging.ERROR)
    # create oai harvester with a test reader

    harvester_metadata = {
        "code": "test",
        "baseurl": (Path(__file__).parent / "harvest_data.json").as_uri(),
        "metadataprefix": "test",
        "comment": "comment",
        "name": "Test harvester",
        "setspecs": "test",
        "loader": "file",
        "transformers": [
            "error_transformer",
            "set_community{community=default}",
        ],
        "writers": [
            "service{service=test_model,update=true}",
            "publish{service=test_model,direct_call=true}",
        ],
        "batch_size": 6,
    }
    harvester = _add_harvester(harvester_metadata)

    # run the harvester synchronously

    run_id = harvest(
        harvester,
        all_records=True,
        on_background=False,
        identifiers=None,
    )

    # check the harvested data
    print(f"{run_id=}")
    oai_run = OAIHarvesterRun.query.get(run_id)
    print(f"{oai_run=}")

    oai_records = get_oai_records(run_id)

    assert len(oai_records) == 3

    assert oai_records.keys() == {"2", "3", "4"}

    assert oai_records["2"].errors
    assert oai_records["2"].errors == [
        {
            "code": "validation",
            "message": "Length must be between 1 and 6.",
            "location": "metadata.title",
        }
    ]

    assert oai_records["2"].original_data == {
        "metadata": {"title": "too long title"},
        "parent": {"communities": {"default": "default"}},
        "files": {"enabled": False},
    }

    assert oai_records["3"].errors == [
        {
            "code": "validation",
            "message": "Unknown field.",
            "location": "extra",
        }
    ]

    assert oai_records["3"].original_data == {
        "extra": "blah",
        "parent": {"communities": {"default": "default"}},
    }

    assert oai_records["4"].errors == [
        {
            "code": "TE",
            "message": "Error in transformer",
            "location": "transformer",
            "info": {
                "transformer-specific-message": "tells transformer to raise error on this record"
            },
        }
    ]

    ok_records = get_ok_records()

    # the other records were either skipped, failed or deleted
    assert ok_records.keys() == {"1"}
    assert ok_records["1"]["oai"] == {
        "harvest": {"datestamp": "2000-01-01", "identifier": "1"}
    }

    # run the harvester again, fix the first error
    harvester_metadata = {
        "code": "test2",
        "baseurl": (Path(__file__).parent / "harvest_data2.json").as_uri(),
        "metadataprefix": "test",
        "comment": "comment",
        "name": "Test harvester",
        "setspecs": "test",
        "loader": "file",
        "transformers": [
            "error_transformer",
            "set_community{community=default}",
        ],
        "writers": [
            "service{service=test_model,update=true}",
            "publish{service=test_model,direct_call=true}",
        ],
        "batch_size": 6,
    }
    harvester = _add_harvester(harvester_metadata)

    # Fix the record #2

    run_id = harvest(
        harvester,
        all_records=True,
        on_background=False,
        identifiers=None,
    )

    ok_records = get_ok_records()
    assert ok_records.keys() == {"1", "2"}
    assert ok_records["2"]["oai"] == {
        "harvest": {"datestamp": "2000-01-30", "identifier": "2"}
    }
    assert ok_records["2"]["metadata"]["title"] == "oktit"
    assert ok_records["1"]["metadata"]["title"] == "corr2"

    oai_records = get_oai_records(run_id)
    assert len(oai_records) == 0

    all_oai_records = {
        r["oai_identifier"]: r
        for r in OAIHarvestedRecord.query.filter(
            OAIHarvestedRecord.run_id == run_id,
            OAIHarvestedRecord.has_errors.is_(True),
        ).all()
    }
    assert "2" not in all_oai_records


def get_oai_records(run_id: str) -> dict[str, OAIHarvestedRecord]:
    return {
        x.oai_identifier: x
        for x in OAIHarvestedRecord.query.filter_by(
            run_id=run_id, has_errors=True
        ).all()
    }


def get_ok_records():
    from test_model.proxies import current_service as test_model_service

    test_model_service.indexer.refresh()

    ok_records = list(test_model_service.scan(system_identity).hits)
    ok_records = {x["oai"]["harvest"]["identifier"]: x for x in ok_records}
    return ok_records


def test_harvest_performance(app, db, search_clear, default_community):
    # create oai harvester with a test reader
    data_count = 200
    batch_size = 50
    harvester_metadata = {
        "code": "test",
        "baseurl": (Path(__file__).parent / "harvest_data.json").as_uri(),
        "metadataprefix": "test",
        "comment": "comment",
        "name": "Test harvester",
        "batch_size": batch_size,
        "setspecs": "test",
        "loader": f"test_data{{count={data_count}}}",
        "transformers": [
            "error_transformer",
            "set_community{community=default}",
        ],
        "writers": [
            "service{service=test_model,update=true}",
            "publish{service=test_model,direct_call=true}",
        ],
    }
    harvester = _add_harvester(harvester_metadata)

    # run the harvester synchronously
    run_id = harvest(
        harvester,
        all_records=True,
        on_background=False,
        identifiers=None,
        title="Test harvest",
    )
    pprint(get_oai_records(run_id))
    run = OAIHarvesterRun.query.get(run_id)
    assert run.status == "ok"
    assert run.records == 200
    assert run.finished_records == 200
    assert run.ok_records == 200
    assert run.failed_records == 0
    assert run.start_time is not None
    assert run.end_time is not None
    assert run.last_update_time == run.end_time
    assert run.title == "Test harvest"

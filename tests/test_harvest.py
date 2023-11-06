from pathlib import Path
from pprint import pprint

from invenio_access.permissions import system_identity

from oarepo_oaipmh_harvester.cli import _add_harvester
from oarepo_oaipmh_harvester.harvester import harvest
from oarepo_oaipmh_harvester.oai_batch.proxies import current_service as batch_service
from oarepo_oaipmh_harvester.oai_record.proxies import (
    current_service as oai_record_service,
)
from oarepo_oaipmh_harvester.oai_run.proxies import current_service as run_service


def test_harvest_synchronous(app, db, record_service, client, search_clear):
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
        "transformers": ["error_transformer"],
        "writer": "service{service=simple_model}",
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
    oai_run = run_service.read(system_identity, run_id).data
    print(f"{oai_run=}")

    batches = batch_service.scan(
        system_identity,
        params={"facets": {"run_id": [run_id]}},
    )
    oai_records = {}
    for batch in batches.hits:
        batch_id = batch["id"]
        for r in oai_record_service.scan(
            system_identity,
            params={"facets": {"batch_id": [batch_id]}},
        ).hits:
            oai_records[r["oai_identifier"]] = r
    pprint(oai_records)

    # check the created records
    assert "errors" not in oai_records["1"]
    record_pid = oai_records["1"]["local_identifier"]
    record = record_service.read(system_identity, record_pid)
    assert record.data["title"] == "corr"

    assert "errors" in oai_records["2"]
    assert oai_records["2"]["errors"] == [
        {
            "code": "MARHSMALLOW",
            "location": "title",
            "message": "Length must be between 1 and 5.",
        }
    ]
    assert oai_records["2"]["entry"] == {"title": "too long title"}

    assert "errors" in oai_records["3"]
    assert oai_records["3"]["errors"] == [
        {"code": "MARHSMALLOW", "location": "extra", "message": "Unknown field."}
    ]
    assert oai_records["3"]["entry"] == {"extra": "blah"}

    assert "errors" in oai_records["4"]
    assert oai_records["4"]["errors"] == [
        {
            "code": "TE",
            "info": {
                "transformer-specific-message": "tells transformer to raise error on this record"
            },
            "location": "transformer",
            "message": "Error in transformer",
        }
    ]
    assert oai_records["4"]["entry"] == {
        "transformer": "tells transformer to raise error on this record"
    }

    # local identifier not here as the record has been deleted
    assert "local_identifier" not in oai_records["5"]
    assert oai_records["5"]["context"]["oai"]["deleted"]

    # check batch size works. in fact, #6 should have two batches in historical version)
    # so that the check should be more thorough
    assert oai_records["4"]["batch"]["id"] != oai_records["6"]["batch"]["id"]

    # local identifier not here as the record has been deleted
    assert "local_identifier" not in oai_records["6"]
    assert oai_records["6"]["context"]["oai"]["deleted"]


def test_harvest_performance(app, db, record_service, search_clear):
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
        "transformers": ["error_transformer"],
        "writer": "service{service=simple_model}",
    }
    harvester = _add_harvester(harvester_metadata)

    # run the harvester synchronously
    run_id = harvest(
        harvester,
        all_records=True,
        on_background=False,
        identifiers=None,
    )
    run = run_service.read(system_identity, run_id).data
    assert run["status"] == "O"

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


def test_harvest_synchronous(app, db, client, search_clear):
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
        "writer": "service{service=test_model}",
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

    batches = list(
        batch_service.scan(
            system_identity,
            params={"q": f'run.id:"{run_id}"'},
        ).hits
    )

    oai_records = get_oai_records(run_id)

    assert len(oai_records) == 3

    assert oai_records.keys() == {"2", "3", "4"}

    assert "errors" in oai_records["2"]
    assert (
        "metadata.title: Length must be between 1 and 6" in oai_records["2"]["errors"]
    )

    assert oai_records["2"]["entry"] == {
        "metadata": {"title": "too long title"},
        "oai": {"harvest": {"datestamp": "2000-01-02", "identifier": "2"}},
    }

    assert "errors" in oai_records["3"]
    assert "extra: Unknown field" in oai_records["3"]["errors"]

    assert oai_records["3"]["entry"] == {
        "extra": "blah",
        "oai": {"harvest": {"datestamp": "2000-01-03", "identifier": "3"}},
    }

    pprint(oai_records["3"])

    assert "errors" in oai_records["4"]
    assert (
        "transformer: Error in transformer - {'transformer-specific-message': 'tells transformer to raise error on this record'}"
        in oai_records["4"]["errors"]
    )
    assert oai_records["4"]["entry"] == {
        "oai": {"harvest": {"datestamp": "2000-01-03", "identifier": "4"}},
        "transformer": "tells transformer to raise error on this record",
    }

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
        "transformers": ["error_transformer"],
        "writer": "service{service=test_model}",
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

    oai_records = get_oai_records(run_id)
    assert len(oai_records) == 0

    all_oai_records = {
        r["oai_identifier"]: r
        for r in oai_record_service.scan(
            system_identity,
        ).hits
    }
    assert "2" not in all_oai_records


def get_oai_records(run_id):
    batches = list(
        batch_service.scan(
            system_identity,
            params={"q": f'run.id:"{run_id}"'},
        ).hits
    )
    oai_records = {}
    for batch in batches:
        batch_id = batch["id"]
        for r in oai_record_service.scan(
            system_identity,
            params={"q": f'batch.id:"{batch_id}"'},
        ).hits:
            oai_records[r["oai_identifier"]] = r
    return oai_records


def get_ok_records():
    from test_model.proxies import current_service as test_model_service

    ok_records = list(test_model_service.scan(system_identity).hits)
    ok_records = {x["oai"]["harvest"]["identifier"]: x for x in ok_records}
    return ok_records


def test_harvest_performance(app, db, search_clear):
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
        "writer": "service{service=test_model}",
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
    run = run_service.read(system_identity, run_id).data
    assert run["status"] == "O"
    assert run["total_batches"] == 4
    assert run["finished_batches"] == 4
    assert run["created_batches"] == 4
    assert run["manual"] is False
    assert run["errors"] == 0
    assert run["started"] is not None
    assert run["finished"] is not None
    assert run["created"] is not None
    assert run["updated"] is not None
    assert run["title"] == "Test harvest"

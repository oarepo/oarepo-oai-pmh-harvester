from pathlib import Path
from pprint import pprint

import pytest
from invenio_access.permissions import system_identity
from invenio_pidstore.errors import PIDDeletedError

from oarepo_oaipmh_harvester.cli import _add_harvester
from oarepo_oaipmh_harvester.harvester import harvest
from oarepo_oaipmh_harvester.oai_batch.proxies import current_service as batch_service
from oarepo_oaipmh_harvester.oai_record.proxies import (
    current_service as oai_record_service,
)
from oarepo_oaipmh_harvester.oai_run.proxies import current_service as run_service


def test_harvest_synchronous(app, db, record_service, client, search_clear):
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
    def progress(**kwargs):
        print(kwargs)

    run_id = harvest(
        harvester,
        all_records=True,
        on_background=False,
        identifiers=None,
        progress_callback=progress,
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
    record_pid = oai_records["1"]["context"]["pid"]
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

    record_pid = oai_records["5"]["context"]["pid"]
    with pytest.raises(PIDDeletedError):
        record_service.read(system_identity, record_pid)

    # check batch size works. in fact, #6 should have two batches in historical version)
    # so that the check should be more thorough
    assert oai_records["4"]["batch"]["id"] != oai_records["6"]["batch"]["id"]

    record_pid = oai_records["6"]["context"]["pid"]
    with pytest.raises(PIDDeletedError):
        record_service.read(system_identity, record_pid)


def test_harvest_performance(app, db, record_service, search_clear):
    # create oai harvester with a test reader
    data_count = 1000
    batch_size = 100
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
    def progress(*args, **kwargs):
        print(args, kwargs)

    run_id = harvest(
        harvester,
        all_records=True,
        on_background=False,
        identifiers=None,
        progress_callback=progress,
    )

from unittest import mock

from oarepo_oai_pmh_harvester.cli import run, _run_internal
from tests.helpers import mock_harvest


def test_run(load_entry_points, app, db):
    patch = mock.patch('sickle.app.Sickle.harvest', mock_harvest)
    patch.start()
    _run_internal(provider=("uk",))
    patch.stop()


def test_run_2(load_entry_points, app, db):
    patch = mock.patch('sickle.app.Sickle.harvest', mock_harvest)
    patch.start()
    _run_internal(provider=("uk",), synchronizer=("xoai",), oai=("oai:test.example.com:1585322",))
    _run_internal(provider=("uk",), synchronizer=("xoai",), oai=("oai:test.example.com:1585322",))
    patch.stop()


def test_run_only_fetch(load_entry_points, app, db, index):
    patch = mock.patch('sickle.app.Sickle.harvest', mock_harvest)
    patch.start()
    _run_internal(provider=("uk",), synchronizer=("xoai",), only_fetch=True, index="test_index")
    patch.stop()

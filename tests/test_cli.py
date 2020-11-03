from unittest import mock

from oarepo_oai_pmh_harvester.cli import run
from tests.helpers import mock_harvest


def test_run(load_entry_points, app, db):
    patch = mock.patch('sickle.app.Sickle.harvest', mock_harvest)
    patch.start()
    runner = app.test_cli_runner()
    result = runner.invoke(run, ["-p", "uk"])
    assert result.exit_code == 0
    patch.stop()

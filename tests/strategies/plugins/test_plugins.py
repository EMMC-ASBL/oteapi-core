"""Tests the plugin for loading all plugins."""
# pylint: disable=unused-argument
from pathlib import Path
from warnings import warn

from pytest_mock import MockerFixture  # Temporary - see note below


def test_load_plugins(import_oteapi_modules, mocker: MockerFixture):
    """Test the `plugins.py` plugin."""
    import oteapi.plugins.plugins

    setup_cfg_file = Path(__file__).resolve().parents[3] / "setup.cfg"
    with open(setup_cfg_file, "rt") as setup_cfg:
        entry_point_cfg = setup_cfg.read()

    entry_pts = oteapi.plugins.plugins.get_all_entry_points()
    for ept in entry_pts:
        try:
            assert entry_point_cfg.find(ept) > 0
        # NOTE: Temporary exception handler, remove when irrelevant
        except AssertionError as err:
            # Temporarily ignore installed obsolete names
            if ept.endswith(".image_jpeg"):
                # Obsolete name for the image/jpeg parse strategy
                warn(
                    "Obsolete name for image/jpeg strategy: 'image_jpeg'"
                    " - current name is 'image'",
                    DeprecationWarning,
                    2,
                )
                index = entry_pts.index(ept)
                entry_pts[index] = "oteapi.strategies.parse.image"
                mocker.patch(
                    "oteapi.plugins.plugins.get_all_entry_points",
                    return_value=entry_pts,
                )
            elif ept.endswith(".text_json"):
                # Obsolete name for the application/json parse strategy
                warn(
                    "Obsolete name for application/json strategy: 'text_json'"
                    " - current name is 'application_json'",
                    DeprecationWarning,
                    2,
                )
                index = entry_pts.index(ept)
                entry_pts[index] = "oteapi.strategies.parse.application_json"
                mocker.patch(
                    "oteapi.plugins.plugins.get_all_entry_points",
                    return_value=entry_pts,
                )
            else:
                raise ModuleNotFoundError(ept)

    oteapi.plugins.plugins.load_plugins()

"""test_config_updater.py"""

from __future__ import annotations

import pytest

from oteapi.models.genericconfig import GenericConfig


def test_populate_config_from_session_success():
    """
    Test the successful population of a GenericConfig object
    from a session dictionary using the populate_config_from_session function.
    """
    from oteapi.utils.config_updater import populate_config_from_session

    # Setup
    config = GenericConfig()
    session = {
        "key1": "value1",
        "key2": "value2",
    }

    # Execute
    populate_config_from_session(session, config)

    # Assert
    assert config.configuration["key1"] == "value1"
    assert config.configuration["key2"] == "value2"


def test_populate_config_from_session_conflict():
    """
    Test the behavior of populate_config_from_session function when there's a
    conflict between the values in the session dictionary and the GenericConfig object.
    """
    from oteapi.utils.config_updater import populate_config_from_session

    # Setup
    config = GenericConfig(configuration={"key1": "conflicting_value"})
    session = {
        "key1": "value1",
    }

    # Execute & Assert
    with pytest.raises(ValueError, match=r".*has different value than in session.*"):
        populate_config_from_session(session, config)

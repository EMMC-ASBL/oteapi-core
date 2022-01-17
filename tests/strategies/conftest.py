"""Pytest fixtures for `strategies/`."""
import pytest


@pytest.fixture(scope="session", autouse=True)
def load_plugins() -> None:
    """Load plugins."""
    from oteapi.plugins.plugins import load_plugins

    load_plugins()

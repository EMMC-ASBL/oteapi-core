"""Pytest fixtures for `strategies/`."""
import pytest


@pytest.fixture(scope="session", autouse=True)
def load_strategies() -> None:
    """Load entry points strategies."""
    from oteapi.plugins import load_strategies

    load_strategies(test_for_uniqueness=False)

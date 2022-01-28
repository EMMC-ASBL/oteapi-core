"""Test the `oteapi.plugins.entry_points` module."""
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from importlib.metadata import EntryPoint
    from typing import Callable, Dict, Tuple


def test_get_strategy_entry_points(
    get_local_strategies: "Callable[[str], Tuple[EntryPoint, ...]]",
) -> None:
    """Simple test for `get_strategy_entry_points()`."""
    from oteapi.plugins.entry_points import (
        EntryPointStrategy,
        get_strategy_entry_points,
    )

    strategy_type = "download"
    entry_points = get_local_strategies(strategy_type)

    collection = get_strategy_entry_points(strategy_type)

    assert len(entry_points) == len(collection)
    for entry_point in entry_points:
        strategy_name = entry_point.name[len("oteapi.") :]
        assert strategy_name in collection
        assert EntryPointStrategy(entry_point) == collection[strategy_name]


def test_incorrect_strategy_type() -> None:
    """Ensure `ValueError` is raised for an invalid strategy type for
    `get_strategy_entry_points()."""
    from oteapi.plugins.entry_points import StrategyType, get_strategy_entry_points

    invalid_strategy_type = "test"

    with pytest.raises(ValueError):
        StrategyType(invalid_strategy_type)

    with pytest.raises(
        ValueError,
        match=rf"^Strategy type {invalid_strategy_type!r} is not supported.$",
    ):
        get_strategy_entry_points(invalid_strategy_type)


def test_no_available_strategies(monkeypatch: pytest.MonkeyPatch) -> None:
    """Ensure the collection is empty and everything runs fine otherwise when
    passing a valid entry point, which has no values."""
    from enum import Enum

    from oteapi.plugins import entry_points

    class MockStrategyType(Enum):
        """Mock StrategyType Enum.

        Have a value representing a non-existing strategy.
        """

        TEST = "test"

    monkeypatch.setattr(entry_points, "StrategyType", MockStrategyType)

    collection = entry_points.get_strategy_entry_points(MockStrategyType.TEST)

    assert not collection


def test_enforce_uniqueness_duplicate_strategies(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Ensure `enforce_uniqueness=True` in `get_strategy_entry_points` ensures
    `KeyError` is raised for duplicate strategies, and doesn't raise if `False`."""
    from importlib.metadata import EntryPoint

    from oteapi.plugins import entry_points

    strategy_type = "download"

    def mock_entry_points() -> "Dict[str, Tuple[EntryPoint]]":
        """Mock function for `importlib.metadata.entry_points`."""
        return {
            f"oteapi.{strategy_type}": (
                EntryPoint(
                    name="package_one.file",
                    value="package_one.strategies.file:StandardFileStrategy",
                    group=f"oteapi.{strategy_type}",
                ),
                EntryPoint(
                    name="package_two.file",
                    value="package_two.strategies.file:SpecialFileStrategy",
                    group=f"oteapi.{strategy_type}",
                ),
            )
        }

    monkeypatch.setattr(entry_points, "get_entry_points", mock_entry_points)

    with pytest.raises(KeyError):
        entry_points.get_strategy_entry_points(strategy_type, enforce_uniqueness=True)

    collection = entry_points.get_strategy_entry_points(
        strategy_type, enforce_uniqueness=False
    )

    assert len(collection) == 1

    expected_entry_point_full_name = (
        f"oteapi.{strategy_type}"
        f"{entry_points.EntryPointStrategy.ENTRY_POINT_NAME_SEPARATOR}"
        f"{list(mock_entry_points().values())[0][0].name}"
    )
    assert expected_entry_point_full_name in collection

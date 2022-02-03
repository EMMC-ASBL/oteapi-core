"""Test the `oteapi.plugins.entry_points` module's `EntryPointStrategy*` classes."""
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:  # pragma: no cover
    from importlib.metadata import EntryPoint
    from typing import Any, Callable, Dict, Iterable, Tuple, Union

    MockEntryPoints = Callable[[Iterable[Union[EntryPoint, Dict[str, Any]]]], None]


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


def test_entry_point_name_syntax(
    create_importlib_entry_points: "Callable[[str], Tuple[EntryPoint, ...]]",
) -> None:
    """Test edge-case and invalid entry point names when initializing
    `EntryPointStrategy`s."""
    from oteapi.plugins.entry_points import EntryPointStrategy

    # Invalid entry points:
    # - Entry name doesn't start with package name.
    # - Wrong package + strategy type value separator
    invalid_entry_points = """\
oteapi.download =
  test = test_package:TestStrategy
oteapi.parse =
  test_package:test = test_package:TestStrategy
"""

    # Edge-case entry points:
    # - Weird chars for strategy value
    edge_case_entry_points = """\
oteapi.download =
  package.$t/\\123## = package.weird.name.chars:Test
"""

    for entry_point in create_importlib_entry_points(invalid_entry_points):
        full_name = (
            f"{entry_point.group}"
            f"{EntryPointStrategy.ENTRY_POINT_NAME_SEPARATOR}"
            f"{entry_point.name}"
        )
        with pytest.raises(
            ValueError,
            match=(
                r"^Could not determine package name and/or strategy name for entry "
                rf"point: {full_name}$"
            ),
        ):
            EntryPointStrategy(entry_point)

    for entry_point in create_importlib_entry_points(edge_case_entry_points):
        assert EntryPointStrategy(entry_point)


def test_collection_remove(
    get_local_strategies: "Callable[[str], Tuple[EntryPoint, ...]]",
) -> None:
    """Test `EntryPointStrategyCollection.remove()`."""
    from oteapi.plugins.entry_points import (
        EntryPointStrategy,
        EntryPointStrategyCollection,
    )

    entry_point_strategies = {
        EntryPointStrategy(_) for _ in get_local_strategies("parse")
    }
    assert len(entry_point_strategies) > 3

    collection = EntryPointStrategyCollection(*entry_point_strategies)
    assert len(collection) == len(entry_point_strategies)

    single_entry_point_to_remove = entry_point_strategies.pop()

    collection.remove(single_entry_point_to_remove)
    assert len(collection) == len(entry_point_strategies)
    assert all(_ in collection for _ in entry_point_strategies)

    # Re-remove an entry point from the collection
    # This shouldn't raise, as the collection can be viewed as a set, where `remove`
    # uses the `-=` operator.
    collection.remove(single_entry_point_to_remove)
    assert len(collection) == len(entry_point_strategies)
    assert all(_ in collection for _ in entry_point_strategies)

    multiple_entry_points_to_remove = {entry_point_strategies.pop()}
    while len(entry_point_strategies) > 2:
        multiple_entry_points_to_remove.add(entry_point_strategies.pop())
    assert len(multiple_entry_points_to_remove) > 1

    collection.remove(*multiple_entry_points_to_remove)
    assert len(collection) == len(entry_point_strategies)
    assert all(_ in collection for _ in entry_point_strategies)


def test_collection_contains(
    create_importlib_entry_points: "Callable[[str], Tuple[EntryPoint, ...]]",
) -> None:
    """Test `EntryPointStrategyCollection.__contains__()` /
    `x in EntryPointStrategyCollection()`."""
    from oteapi.plugins.entry_points import (
        EntryPointStrategy,
        EntryPointStrategyCollection,
    )

    entry_points = """\
oteapi.download =
  test.file = test:Test
  test.http = test:Test
  test.ftp = test:Test
"""
    excluded_entry_points = """\
oteapi.parse =
  test.test = test:Test
  test.http = test:Test
"""

    entry_point_strategies = {
        EntryPointStrategy(_) for _ in create_importlib_entry_points(entry_points)
    }
    collection = EntryPointStrategyCollection(*entry_point_strategies)

    # Assert IN
    assert len(collection) == 3
    assert all(_ in collection for _ in entry_point_strategies)
    assert all(_.full_name in collection for _ in entry_point_strategies)
    assert all(_.strategy in collection for _ in entry_point_strategies)
    assert all((_.type.value, _.name) in collection for _ in entry_point_strategies)

    excluded_entry_point_strategies = {
        EntryPointStrategy(_)
        for _ in create_importlib_entry_points(excluded_entry_points)
    }

    # Assert NOT IN
    assert all(_ not in collection for _ in excluded_entry_point_strategies)
    assert all(_.full_name not in collection for _ in excluded_entry_point_strategies)
    assert all(_.strategy not in collection for _ in excluded_entry_point_strategies)
    assert all(
        (_.type.value, _.name) not in collection
        for _ in excluded_entry_point_strategies
    )

    # `name` cannot be used as it does not constitute uniqueness
    assert all(
        _.name not in collection
        for _ in entry_point_strategies.union(excluded_entry_point_strategies)
    )

    sorted(collection)

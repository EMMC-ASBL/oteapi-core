"""Test the `oteapi.plugins.entry_points` module's `EntryPointStrategy*` classes."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    import sys
    from collections.abc import Callable, Iterable
    from typing import Any

    if sys.version_info < (3, 10):
        from importlib_metadata import EntryPoint
    else:
        from importlib.metadata import EntryPoint

    MockEntryPoints = Callable[[Iterable[EntryPoint | dict[str, Any]]], None]


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
    create_importlib_entry_points: Callable[[str], tuple[EntryPoint, ...]],
) -> None:
    """Test edge-case and invalid entry point names when initializing
    `EntryPointStrategy`s."""
    from oteapi.plugins.entry_points import EntryPointStrategy

    # Invalid entry points:
    # - Entry name doesn't start with package name.
    # - Wrong package + strategy type value separator
    # - Invalid package name (must start/end with a letter or number)
    invalid_entry_points = """\
oteapi.download =
  test = test_package:TestStrategy
oteapi.parse =
  test_package:test = test_package:TestStrategy
oteapi.mapping =
  _test_package.test = test_package:TestStrategy
"""

    # Edge-case entry points:
    # - Weird chars for strategy value
    # - Valid non-normalized package names
    edge_case_entry_points = """\
oteapi.download =
  package.$t/\\123## = package.weird.name.chars:Test
oteapi.parse =
  Friendly-Bard.test = friendly_bard:TestStrategy
  FRIENDLY-BARD.test = friendly_bard:TestStrategy
  friendly.bard.test = friendly_bard:TestStrategy
  friendly_bard.test = friendly_bard:TestStrategy
  friendly--bard.test = friendly_bard:TestStrategy
  FrIeNdLy-._.-bArD.test = friendly_bard:TestStrategy
oteapi.mapping =
  7.8-_9.test = 7_8_9:TestStrategy
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
    get_local_strategies: Callable[[str], tuple[EntryPoint, ...]],
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
    create_importlib_entry_points: Callable[[str], tuple[EntryPoint, ...]],
) -> None:
    """Test `EntryPointStrategyCollection.__contains__()` /
    `x in EntryPointStrategyCollection()`."""
    from oteapi.plugins.entry_points import (
        EntryPointStrategy,
        EntryPointStrategyCollection,
        StrategyType,
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

    # General
    assert all(
        _.name not in collection
        for _ in entry_point_strategies.union(excluded_entry_point_strategies)
    )
    assert ("download", "file", "test") not in collection
    assert ("download",) not in collection
    with pytest.raises(ValueError):  # noqa: PT011
        StrategyType("test")
    assert ("test", "file") not in collection


def test_invalid_module(
    create_importlib_entry_points: Callable[[str], tuple[EntryPoint, ...]],
) -> None:
    """Ensure `EntryPointNotFound` is raised if a module cannot be imported."""
    from importlib import import_module

    from oteapi.plugins.entry_points import EntryPointNotFound, EntryPointStrategy

    package = "test"
    invalid_module = "this_module_does_not_exist"
    invalid_class = "Test"
    valid_module = "static.strategies.download"
    entry_points = f"""\
oteapi.download =
  {package}.http = {valid_module}:{invalid_class}
  {package}.test = {invalid_module}:Test
"""

    # Sorts entry points strategies by: strategy type, package, strategy name
    entry_point_strategies = sorted(
        EntryPointStrategy(_) for _ in create_importlib_entry_points(entry_points)
    )
    assert len(entry_point_strategies) == 2
    for index, strategy in enumerate(("http", "test")):
        assert strategy == entry_point_strategies[index].name

    assert import_module(valid_module)
    with pytest.raises(
        EntryPointNotFound,
        match=rf"^{invalid_class} cannot be found in {valid_module}$",
    ):
        entry_point_strategies[0].implementation

    with pytest.raises(
        EntryPointNotFound,
        match=(
            rf"^{invalid_module} cannot be imported\. Did you install the {package!r} "
            r"package\?$"
        ),
    ):
        entry_point_strategies[1].implementation


def test_sorting_priority(
    create_importlib_entry_points: Callable[[str], tuple[EntryPoint, ...]],
) -> None:
    """Ensure `EntryPointStrategy`s are sorted correctly according to the intended
    priority order in `__lt__()`."""
    from oteapi.plugins.entry_points import (
        EntryPointStrategy,
        EntryPointStrategyCollection,
        StrategyType,
    )

    entry_points = """\
oteapi.download =
  test.a = test:Test
  test.b = test:Test
oteapi.parse =
  a.a = test:Test
  b.b = test:Test
"""

    expected_sorting = (
        (StrategyType("download"), "a"),
        (StrategyType("download"), "b"),
        (StrategyType("parse"), "a"),
        (StrategyType("parse"), "b"),
    )

    entry_point_strategies = {
        EntryPointStrategy(_) for _ in create_importlib_entry_points(entry_points)
    }
    collection = EntryPointStrategyCollection()
    collection.exclusive_add(*entry_point_strategies)
    sorted_collection: list[EntryPointStrategy] = sorted(collection)
    assert sorted_collection == sorted(entry_point_strategies)
    for index, strategy in enumerate(expected_sorting):
        assert sorted_collection[index].strategy == strategy

    with pytest.raises(
        NotImplementedError,
        match=rf"^Less than comparison is not implemented for {int} type objects.$",
    ):
        entry_point_strategies.pop() < 2


def test_collection_getitem(
    create_importlib_entry_points: Callable[[str], tuple[EntryPoint, ...]],
) -> None:
    """Test `EntryPointStrategyCollection.__getitem__()` /
    `EntryPointStrategyCollection()[x]`."""
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
    non_existing_entry_points = """\
oteapi.parse =
  test.test = test:Test
  test.http = test:Test
"""

    entry_point_strategies = {
        EntryPointStrategy(_) for _ in create_importlib_entry_points(entry_points)
    }
    collection = EntryPointStrategyCollection(*entry_point_strategies)
    non_existing_entry_points_strategies = {
        EntryPointStrategy(_)
        for _ in create_importlib_entry_points(non_existing_entry_points)
    }

    assert all(
        isinstance(collection[_], EntryPointStrategy) for _ in entry_point_strategies
    )
    assert all(
        isinstance(collection[_.full_name], EntryPointStrategy)
        for _ in entry_point_strategies
    )
    assert all(
        isinstance(collection[_.strategy], EntryPointStrategy)
        for _ in entry_point_strategies
    )
    assert all(
        isinstance(collection[(_.type.value, _.name)], EntryPointStrategy)
        for _ in entry_point_strategies
    )

    for entry_point_strategy in non_existing_entry_points_strategies:
        with pytest.raises(KeyError, match=r"not found in"):
            collection[entry_point_strategy]
        with pytest.raises(
            RuntimeError,
            match=(
                r"not found in .+, which is a "
                r"requirement for the _get_entry_point method\.$"
            ),
        ):
            collection._get_entry_point(entry_point_strategy.full_name)

    with pytest.raises(
        TypeError,
        match=(
            r"^key should either be of type EntryPointStrategy, a string of the full "
            r"name or a strategy tuple\.$"
        ),
    ):
        collection[2]


def test_collection_eq(
    create_importlib_entry_points: Callable[[str], tuple[EntryPoint, ...]],
) -> None:
    """Test `EntryPointStrategyCollection.__eq__()` /
    `EntryPointStrategyCollection() == EntryPointStrategyCollection()`."""
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

    entry_point_strategies = {
        EntryPointStrategy(_) for _ in create_importlib_entry_points(entry_points)
    }
    collection = EntryPointStrategyCollection()
    collection.exclusive_add(*entry_point_strategies)

    assert collection == EntryPointStrategyCollection(*list(entry_point_strategies))
    assert collection != 2
    assert collection != EntryPointStrategyCollection(
        *list(entry_point_strategies)[:-1]
    )


def test_collection_str_repr(
    create_importlib_entry_points: Callable[[str], tuple[EntryPoint, ...]],
) -> None:
    """Test `EntryPointStrategyCollection.__str__()` and `.__repr__()` /
    `str(EntryPointStrategyCollection())` or `repr()`."""
    from oteapi.plugins.entry_points import (
        EntryPointStrategy,
        EntryPointStrategyCollection,
    )

    entry_points = """\
oteapi.download =
  test.file = test:Test
  test.http = test:Test
oteapi.parse =
  test.text/plain = test:Test
"""

    entry_point_strategies = tuple(
        sorted(
            EntryPointStrategy(_) for _ in create_importlib_entry_points(entry_points)
        )
    )
    collection = EntryPointStrategyCollection(*entry_point_strategies)

    assert (
        str(collection)
        == f"<{collection.__class__.__name__}: Strategies=download (2), parse (1)>"
    )
    assert (
        repr(collection)
        == f"{collection.__class__.__name__}(*{entry_point_strategies!r})"
    )


def test_strategy_eq(
    create_importlib_entry_points: Callable[[str], tuple[EntryPoint, ...]],
) -> None:
    """Test `EntryPointStrategy.__eq__()` /
    `EntryPointStrategy() == EntryPointStrategy()`."""
    from oteapi.plugins.entry_points import EntryPointStrategy

    entry_points = """\
oteapi.download =
  test.file = test:Test
  test.http = test:Test
  test.ftp = test:Test
"""

    parsed_entry_points = create_importlib_entry_points(entry_points)
    strategies = [EntryPointStrategy(_) for _ in parsed_entry_points]

    for index, strategy in enumerate(strategies):
        assert strategy == EntryPointStrategy(parsed_entry_points[index])
    assert strategies[0] != 2
    assert strategies[0] != strategies[1]

    assert sorted(strategies + strategies) == sorted(strategies + strategies)

"""Test the `oteapi.plugins.entry_points` module generally."""
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from importlib.metadata import EntryPoint
    from typing import Any, Callable, Dict, Iterable, Tuple, Union

    MockEntryPoints = Callable[[Iterable[Union[EntryPoint, Dict[str, Any]]]], None]


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
        assert (strategy_type, strategy_name) in collection
        assert (
            EntryPointStrategy(entry_point)
            == collection[(strategy_type, strategy_name)]
        )


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


def test_enforce_uniqueness_duplicate_strategies(
    mock_importlib_entry_points: "MockEntryPoints",
) -> None:
    """Ensure `enforce_uniqueness=True` in `get_strategy_entry_points` ensures
    `KeyError` is raised for duplicate strategies, and doesn't raise if `False`."""
    strategy_type = "download"
    test_entry_points = [
        {
            "name": "package_one.file",
            "value": "package_one.strategies.file:StandardFileStrategy",
            "group": f"oteapi.{strategy_type}",
        },
        {
            "name": "package_two.file",
            "value": "package_two.strategies.file:SpecialFileStrategy",
            "group": f"oteapi.{strategy_type}",
        },
    ]
    # Must be called prior to importing anything from `oteapi`
    mock_importlib_entry_points(test_entry_points)

    from oteapi.plugins.entry_points import (
        EntryPointStrategy,
        get_strategy_entry_points,
    )

    with pytest.raises(KeyError):
        get_strategy_entry_points(strategy_type, enforce_uniqueness=True)

    collection = get_strategy_entry_points(strategy_type, enforce_uniqueness=False)

    assert len(collection) == 1

    expected_entry_point_full_name = (
        f"oteapi.{strategy_type}"
        f"{EntryPointStrategy.ENTRY_POINT_NAME_SEPARATOR}"
        f"{test_entry_points[0].get('name', '')}"
    )
    assert expected_entry_point_full_name in collection


def test_strategytype_methods() -> None:
    """Test the `StrategyType` methods return the expected values."""
    from oteapi.plugins.entry_points import StrategyType

    expected_values = {
        "download": "scheme",
        "filter": "filterType",
        "function": "functionType",
        "mapping": "mappingType",
        "parse": "mediaType",
        "resource": "accessService",
        "transformation": "transformationType",
    }

    for strategy_name, strategy_type in expected_values.items():
        strategy = StrategyType(strategy_name)
        assert strategy_type == strategy.map_to_field()
        assert strategy == StrategyType.map_from_field(strategy_type)
        assert strategy == StrategyType.init(strategy_type)
        assert strategy == StrategyType.init(strategy_name)
        assert strategy == StrategyType.init(strategy)

        with pytest.raises(ValueError):
            StrategyType(strategy_type)

    assert set(expected_values.keys()) == set(StrategyType.all_values())


def test_eval_custom_classes() -> None:
    """Check the custom classes can be re-invoked using `eval(repr())`."""
    # pylint: disable=eval-used,protected-access
    from importlib.metadata import EntryPoint

    from oteapi.plugins.entry_points import (
        EntryPointStrategy,
        EntryPointStrategyCollection,
    )

    test_entry_point = EntryPoint(
        name="test.test",
        value="test:Test",
        group="oteapi.download",
    )

    normal_strategy_cls = EntryPointStrategy(test_entry_point)
    eval_strategy_cls = eval(repr(normal_strategy_cls))
    assert isinstance(eval_strategy_cls, EntryPointStrategy)
    assert normal_strategy_cls == eval_strategy_cls
    assert (
        normal_strategy_cls._entry_point
        == eval_strategy_cls._entry_point
        == test_entry_point
    )

    normal_collection_cls = EntryPointStrategyCollection(normal_strategy_cls)
    eval_collection_cls = eval(repr(normal_collection_cls))
    assert isinstance(eval_collection_cls, EntryPointStrategyCollection)
    assert normal_collection_cls == eval_collection_cls
    assert (
        normal_collection_cls._entry_points
        == eval_collection_cls._entry_points
        == {normal_strategy_cls}
    )


@pytest.mark.parametrize(
    "enforce_uniqueness", (True, False), ids=("uniqueness", "no uniqueness")
)
def test_duplicate_entry_points(
    mock_importlib_entry_points: "MockEntryPoints",
    enforce_uniqueness: bool,
) -> None:
    """Ensure duplicate entry points does not result in an error.

    Note: This is for duplicate entry points, NOT entry point _strategies_.
    """
    strategy_type = "download"
    test_entry_points = [
        {
            "name": "package_one.file",
            "value": "package_one.strategies.file:FileStrategy",
            "group": f"oteapi.{strategy_type}",
        },
        {
            "name": "package_two.http",
            "value": "package_two.strategies.http:HTTPStrategy",
            "group": f"oteapi.{strategy_type}",
        },
    ]
    # Must be called prior to importing anything from `oteapi`
    mock_importlib_entry_points(test_entry_points + test_entry_points)

    from oteapi.plugins.entry_points import (
        EntryPointStrategy,
        get_entry_points,
        get_strategy_entry_points,
    )

    assert len(get_entry_points().get(f"oteapi.{strategy_type}", [])) == 2 * len(
        test_entry_points
    )

    collection = get_strategy_entry_points(
        strategy_type, enforce_uniqueness=enforce_uniqueness
    )

    assert len(collection) == len(test_entry_points)

    for test_entry_point in test_entry_points:
        assert (
            f"oteapi.{strategy_type}"
            f"{EntryPointStrategy.ENTRY_POINT_NAME_SEPARATOR}"
            f"{test_entry_point.get('name', '')}"
        ) in collection

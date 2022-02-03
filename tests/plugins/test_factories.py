"""Test the `oteapi.plugins.factories` module generally."""
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:  # pragma: no cover
    from importlib.metadata import EntryPoint
    from typing import Any, Callable, Dict, Iterable, Type, Union

    from oteapi.models import StrategyConfig
    from oteapi.plugins.entry_points import StrategyType

    MockEntryPoints = Callable[[Iterable[Union[EntryPoint, Dict[str, Any]]]], None]


def test_load_strategies(mock_importlib_entry_points: "MockEntryPoints") -> None:
    """Test `StrategyFactory.load_strategies()`."""
    strategy_type = "download"
    entry_points = [
        {
            "name": "test.http",
            "value": "tests.static.strategies.download:HTTPSStrategy",
            "group": f"oteapi.{strategy_type}",
        },
    ]

    mock_importlib_entry_points(entry_points)

    from oteapi.plugins.entry_points import (
        EntryPointStrategy,
        EntryPointStrategyCollection,
        StrategyType,
        get_entry_points,
    )
    from oteapi.plugins.factories import StrategyFactory, load_strategies

    load_strategies()

    assert len(StrategyFactory.strategy_create_func) == len(StrategyType)
    assert StrategyFactory.strategy_create_func[
        StrategyType(strategy_type)
    ] == EntryPointStrategyCollection(
        *(EntryPointStrategy(_) for _ in get_entry_points()[f"oteapi.{strategy_type}"])
    )
    for key in StrategyFactory.strategy_create_func:
        if key != StrategyType(strategy_type):
            assert (
                StrategyFactory.strategy_create_func[key]
                == EntryPointStrategyCollection()
            )


def test_load_strategies_fails(mock_importlib_entry_points: "MockEntryPoints") -> None:
    """Test `StrategyFactory.load_strategies()` fails when expected to."""
    strategy_type = "download"
    not_importable_entry_points = [
        {
            "name": "package_one.http",
            "value": "test:Test",
            "group": f"oteapi.{strategy_type}",
        },
        {
            "name": "package_two.http",
            "value": "test:Test",
            "group": f"oteapi.{strategy_type}",
        },
    ]

    mock_importlib_entry_points(not_importable_entry_points)

    from oteapi.plugins.factories import load_strategies

    with pytest.raises(KeyError):
        load_strategies(test_for_uniqueness=True)

    load_strategies(test_for_uniqueness=False)


@pytest.mark.usefixtures("load_test_strategies")
def test_create_strategy(
    get_strategy_config: "Callable[[Union[StrategyType, str]], Type[StrategyConfig]]",
) -> None:
    """Test `StrategyFactory.make_strategy()`."""
    from oteapi.plugins.entry_points import StrategyType
    from oteapi.plugins.factories import StrategyFactory, create_strategy

    for strategy_type, collection in StrategyFactory.strategy_create_func.items():
        for entry_point in collection:
            strategy = create_strategy(
                strategy_type=strategy_type,
                config=(
                    get_strategy_config(strategy_type)(
                        downloadUrl=f"{entry_point.name}://example.org"
                        if entry_point.type == StrategyType.DOWNLOAD
                        else "https",
                        mediaType=entry_point.name
                        if entry_point.type == StrategyType.PARSE
                        else "text/html",
                        accessUrl="https://example.org",
                        accessService=entry_point.name
                        if entry_point.type == StrategyType.RESOURCE
                        else "example.org",
                    )
                    if strategy_type
                    in (
                        StrategyType.DOWNLOAD,
                        StrategyType.PARSE,
                        StrategyType.RESOURCE,
                    )
                    else get_strategy_config(strategy_type)(
                        **{entry_point.type.value: entry_point.name}
                    )
                ),
            )
            assert hasattr(strategy, f"{strategy_type.value}_config")

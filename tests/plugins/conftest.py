"""Pytest fixture for all `oteapi.plugins` tests."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from collections.abc import Callable, Iterable
    from importlib.metadata import EntryPoint
    from typing import Any

    from oteapi.models import StrategyConfig
    from oteapi.plugins.entry_points import StrategyType

    MockEntryPoints = Callable[[Iterable[EntryPoint | dict[str, Any]]], None]


@pytest.fixture
def get_local_strategies() -> Callable[[str], tuple[EntryPoint, ...]]:
    """Retrieve all entry points for strategy type from oteapi-core."""
    from importlib.metadata import entry_points

    from oteapi.plugins.entry_points import StrategyType

    def _get_local_strategies(
        strategy_type: StrategyType | str,
    ) -> tuple[EntryPoint, ...]:
        """Get oteapi-core entry points from strategy type.

        Parameters:
            strategy_type: The strategy type for which to retrieve all oteapi-core
                entry points.

        Returns:
            A tuple of importlib.metadata API EntryPoints for the given strategy type.

        """
        try:
            strategy_type = StrategyType.init(strategy_type)
        except ValueError:
            pytest.fail(
                "Incorrect `strategy_type` passed to `get_local_strategies` fixture. "
                f"Valid values: {StrategyType.all_values()}"
            )

        return tuple(
            _
            for _ in entry_points(group=f"oteapi.{strategy_type.value}")
            if _.name.startswith("oteapi.")
        )

    return _get_local_strategies


@pytest.fixture
def _load_test_strategies(
    create_importlib_entry_points: Callable[[str], tuple[EntryPoint, ...]],
    mock_importlib_entry_points: MockEntryPoints,
) -> None:
    """Load all strategies under `tests/static/strategies/`."""
    setup_cfg = """\
oteapi.download =
  oteapi_tests.http = static.strategies.download:DownloadTestStrategy
  oteapi_tests.https = static.strategies.download:DownloadTestStrategy
oteapi.filter =
  oteapi_tests.query_parameters = static.strategies.filter:FilterTestStrategy
oteapi.function =
  oteapi_tests.render = static.strategies.function:FunctionTestStrategy
oteapi.mapping =
  oteapi_tests.html = static.strategies.mapping:MappingTestStrategy
oteapi.parse =
  oteapi_tests.parser/json = static.strategies.parse:ParseTestStrategy
oteapi.resource =
  oteapi_tests.resource/url = static.strategies.resource:ResourceTestStrategy
oteapi.transformation =
  oteapi_tests.render = static.strategies.transformation:TransformationTestStrategy
"""
    entry_points = create_importlib_entry_points(setup_cfg)
    mock_importlib_entry_points(entry_points)

    from oteapi.plugins.factories import load_strategies

    load_strategies()


@pytest.fixture
def get_strategy_config() -> Callable[[StrategyType | str], type[StrategyConfig]]:
    """Get the strategy configuration model class."""
    from oteapi.models import (
        FilterConfig,
        FunctionConfig,
        MappingConfig,
        ParserConfig,
        ResourceConfig,
        TransformationConfig,
    )
    from oteapi.plugins.entry_points import StrategyType

    def _get_config(strategy: StrategyType | str) -> type[StrategyConfig]:
        """Return a `StrategyConfig` class for the given `StrategyType`.

        Parameters:
            strategy: A valid strategy, either as the `StrategyType` enumeration or a
                string to be used with `StrategyType.init()`.

        Returns:
            A valid test strategy-specific configuration class.

        """
        try:
            strategy = StrategyType.init(strategy)
        except ValueError:
            pytest.fail(
                "Incorrect `strategy_type` passed to `get_local_strategies` fixture. "
                f"Valid values: {StrategyType.all_values()}"
            )

        return {
            StrategyType.DOWNLOAD: ResourceConfig,
            StrategyType.FILTER: FilterConfig,
            StrategyType.FUNCTION: FunctionConfig,
            StrategyType.MAPPING: MappingConfig,
            StrategyType.PARSE: ParserConfig,
            StrategyType.RESOURCE: ResourceConfig,
            StrategyType.TRANSFORMATION: TransformationConfig,
        }[strategy]

    return _get_config

"""Pytest fixture for all `oteapi.plugins` tests."""
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from importlib.metadata import EntryPoint
    from typing import Callable, Tuple, Union


@pytest.fixture
def get_local_strategies() -> "Callable[[str], Tuple[EntryPoint, ...]]":
    """Retrieve all entry points for strategy type from oteapi-core."""
    from importlib.metadata import entry_points

    from oteapi.plugins.entry_points import StrategyType

    def _get_local_strategies(
        strategy_type: "Union[StrategyType, str]",
    ) -> "Tuple[EntryPoint, ...]":
        """Get oteapi-core entry points from strategy type.

        Parameters:
            strategy_type: The strategy type for which to retrieve all oteapi-core
                entry points.

        Returns:
            A tuple of importlib.metadata API EntryPoints for the given strategy type.

        """
        try:
            strategy_type = StrategyType(strategy_type)
        except ValueError:
            pytest.fail(
                "Incorrect `strategy_type` passed to `get_local_strategies` fixture. "
                f"Valid values: {StrategyType.all_values()}"
            )

        return tuple(
            _
            for _ in entry_points()[f"oteapi.{strategy_type.value}"]
            if _.name.startswith("oteapi.")
        )

    return _get_local_strategies

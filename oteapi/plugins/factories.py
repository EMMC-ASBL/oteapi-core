"""Factory class for registering and creating strategy instances.

Factory wrapper methods for creating the individual strategies.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, get_args

from oteapi.models import StrategyConfig
from oteapi.plugins.entry_points import StrategyType, get_strategy_entry_points

if TYPE_CHECKING:  # pragma: no cover
    from typing import Any

    from oteapi.interfaces import IStrategy
    from oteapi.plugins.entry_points import EntryPointStrategyCollection


class StrategiesNotLoaded(Exception):
    """Entry point strategies have not been loaded, run
    [`load_strategies()`][oteapi.plugins.factories.load_strategies]."""


class StrategyFactory:
    """Decorator-based Factory class.

    Attributes:
        strategy_create_func (Dict[StrategyType, EntryPointStrategyCollection]): An
            in-memory cache of all registered strategies.

    """

    strategy_create_func: dict[StrategyType, EntryPointStrategyCollection]

    @classmethod
    def make_strategy(
        cls,
        config: StrategyConfig | dict[str, Any],
        strategy_type: StrategyType | str,
    ) -> IStrategy:
        """Instantiate a strategy in a context class.

        Parameters:
            config: A strategy configuration.
            strategy_type: The strategy type, e.g., `"scheme"`, `"mediaType"`, ... or
                `"download"`, `"parse"`, ...
                See the [`StrategyType`][oteapi.plugins.entry_points.StrategyType]
                enumeration for a definition of valid strategy types.

        Raises:
            NotImplementedError: If the strategy cannot be found.
            ValueError: If the `strategy_type` is not a valid strategy type.
                See the [`StrategyType`][oteapi.plugins.entry_points.StrategyType]
                enumeration for a definition of valid strategy types.
            StrategiesNotLoaded: If the entry point strategies have not been loaded.

        Returns:
            An instantiated strategy. The strategy is instantiated with the provided
            configuration, through the `config` parameter.

        """
        if not hasattr(cls, "strategy_create_func"):
            raise StrategiesNotLoaded(
                "Strategies have not been loaded, run `load_strategies()` or "
                "`StrategyFactory.load_strategies()`."
            )

        if isinstance(strategy_type, str):
            try:
                strategy_type = StrategyType.init(strategy_type)
            except ValueError as exc:
                raise ValueError(
                    f"Strategy type {strategy_type!r} is not supported."
                ) from exc
        elif not isinstance(strategy_type, StrategyType):
            raise TypeError(
                "strategy_type should be either of type StrategyType or a string."
            )

        # 'config': Must be a dict when instantiating the strategy's implementation.
        # 'config_model': Is used to retrieve the correct strategy requested.
        # Furthermore, creating 'config_model' ensures that the config is valid with
        # respect to the strategy type, further reducing the risk of incorrect logical
        # conclusions.
        if isinstance(config, dict):
            config_model = strategy_type.config_cls(**config)
        elif isinstance(config, get_args(StrategyConfig)):
            config_model = config
            config = config.model_dump(mode="json", exclude_unset=True)
        else:
            raise TypeError("config should be either of type StrategyConfig or a dict.")

        strategy_name: str = cls._get_strategy_name(config_model, strategy_type)

        if (strategy_type, strategy_name) in cls.strategy_create_func[strategy_type]:
            return cls.strategy_create_func[strategy_type][
                (strategy_type, strategy_name)
            ].implementation(
                config  # type: ignore[arg-type]
            )
        raise NotImplementedError(
            f"The {strategy_type.value} strategy {strategy_name!r} does not exist."
        )

    @classmethod
    def _get_strategy_name(
        cls,
        config: StrategyConfig,
        strategy_type: StrategyType,
    ) -> str:
        """Return the strategy name through the config.

        This is a method to accommodate strategy type-specific quirks to retrieve the
        strategy name.

        Parameters:
            config: A strategy configuration.
            strategy_type: The strategy type as initialized in `make_strategy()`.

        Returns:
            The strategy name provided in the configuration.

        """
        if strategy_type == StrategyType.DOWNLOAD:
            return (
                config.downloadUrl.scheme  # type: ignore[union-attr]
                if config.downloadUrl is not None  # type: ignore[union-attr]
                else ""
            )
        return getattr(config, strategy_type.map_to_field(), "")

    @classmethod
    def load_strategies(cls, test_for_uniqueness: bool = True) -> None:
        """Load strategies from entry points and store in class attribute.

        Important:
            This is not a cached method.
            The importlib.metadata API will be re-requested to load the entry points
            and strategies.

        Note:
            This does *not* import the actual strategy implementations (classes).
            It only loads the strategies from the registerred OTEAPI entry points.

        Raises:
            KeyError: If `test_for_uniqueness` is `True` and an entry point strategy is
                duplicated.

        Parameters:
            test_for_uniqueness: If `True`, this will raise `KeyError` should an entry
                point strategy be duplicated. Otherwise, the first loaded entry point
                strategy will silently become the implementation of choice for the
                duplicated strategy and the duplicates will be ignored.

        """
        cls.strategy_create_func = {
            strategy_type: get_strategy_entry_points(
                strategy_type, enforce_uniqueness=test_for_uniqueness
            )
            for strategy_type in StrategyType
        }

    @classmethod
    def list_loaded_strategies(cls) -> dict[StrategyType, list[str]]:
        """Lists all loaded strategy plugins (endpoints).

        Returns:
            A dictionary where keys are strategy types and values are lists of
            loaded strategy names for each type.

        Raises:
            StrategiesNotLoaded: If the strategies are not loaded or
                `strategy_create_func` is not properly initialized.
        """
        if not hasattr(cls, "strategy_create_func") or not cls.strategy_create_func:
            raise StrategiesNotLoaded(
                "Strategies are not loaded or `strategy_create_func` is not properly "
                "initialized."
            )

        loaded_strategies = {}
        for strategy_type, strategy_collection in cls.strategy_create_func.items():
            # Assuming each item in the collection has a 'name' attribute or similar
            loaded_strategies[strategy_type] = [
                strategy.name for strategy in strategy_collection
            ]

        return loaded_strategies


def load_strategies(test_for_uniqueness: bool = True) -> None:
    """Proxy function for
    [`StrategyFactory.load_strategies()`][oteapi.plugins.factories.StrategyFactory.load_strategies].

    Parameters:
        test_for_uniqueness: If `True`, this will raise `KeyError` should an entry
            point strategy be duplicated. Otherwise, the first loaded entry point
            strategy will silently become the implementation of choice for the
            duplicated strategy and the duplicates will be ignored.

    """
    StrategyFactory.load_strategies(test_for_uniqueness)


def list_strategies() -> dict[StrategyType, list[str]]:
    """Proxy function for
    [`StrategyFactory.list_loaded_strategies()`][oteapi.plugins.factories.StrategyFactory.list_loaded_strategies].

    Returns:
        A dictionary where keys are strategy types and values are lists of
        loaded strategy names for each type.
    """
    return StrategyFactory.list_loaded_strategies()


def create_strategy(
    strategy_type: StrategyType | str,
    config: StrategyConfig | dict[str, Any],
) -> IStrategy:
    """Proxy function for
    [`StrategyFactory.make_strategy()`][oteapi.plugins.factories.StrategyFactory.make_strategy].

    Parameters:
        strategy_type: A valid strategy type.
            See the [`StrategyType`][oteapi.plugins.entry_points.StrategyType]
            enumeration for a definition of valid strategy types.
        config: A strategy configuration.

    Returns:
        The created strategy.

    """
    return StrategyFactory.make_strategy(config, strategy_type)

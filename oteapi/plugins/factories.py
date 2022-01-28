"""Factory class for registering and creating strategy instances.

Factory wrapper methods for creating the individual strategies.
"""
from typing import TYPE_CHECKING

from oteapi.interfaces import (
    IDownloadStrategy,
    IFilterStrategy,
    IMappingStrategy,
    IParseStrategy,
    IResourceStrategy,
    ITransformationStrategy,
)
from oteapi.plugins.entry_points import StrategyType, get_strategy_entry_points

if TYPE_CHECKING:  # pragma: no cover
    from typing import Dict, Union

    from oteapi.interfaces import IStrategy
    from oteapi.models import (
        FilterConfig,
        MappingConfig,
        ResourceConfig,
        StrategyConfig,
        TransformationConfig,
    )
    from oteapi.plugins.entry_points import EntryPointStrategyCollection


class StrategyFactory:
    """Decorator-based Factory class.

    Attributes:
        strategy_create_func (Dict[StrategyType, EntryPointStrategyCollection]): An
            in-memory cache of all registered strategies.

    """

    strategy_create_func: "Dict[StrategyType, EntryPointStrategyCollection]"

    @classmethod
    def make_strategy(
        cls, config: "StrategyConfig", strategy_type: "Union[StrategyType, str]"
    ) -> "IStrategy":
        """Instantiate a strategy in a context class.

        Parameters:
            config: A strategy configuration.
            strategy_type: The strategy type, e.g., `"scheme"`, `"mediaType"`, ... or
                `"download"`, `"parse"`, ...

        Raises:
            NotImplementedError: If the strategy cannot be found.
            ValueError: If the strategy type is not supported.

        Returns:
            An instantiated strategy. The strategy is instantiated with the provided
            configuration, through the `config` parameter.

        """
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

        strategy_name: str = cls._get_strategy_name(config, strategy_type)

        if strategy_name in cls.strategy_create_func[strategy_type]:
            return cls.strategy_create_func[strategy_type][
                strategy_name
            ].implementation(config)
        raise NotImplementedError(
            f"The {strategy_type.value} strategy {strategy_name!r} does not exist."
        )

    @classmethod
    def _get_strategy_name(
        cls,
        config: "StrategyConfig",
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
            return config.downloadUrl.scheme if config.downloadUrl is not None else ""
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
            It only loads the strategies from the registerred OTE-API entry points.

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


def load_strategies(test_for_uniqueness: bool = True) -> None:
    # pylint: disable=line-too-long
    """Proxy function for
    [`StrategyFactory.load_strategies()`][oteapi.plugins.factories.StrategyFactory.load_strategies].

    Parameters:
        test_for_uniqueness: If `True`, this will raise `KeyError` should an entry
            point strategy be duplicated. Otherwise, the first loaded entry point
            strategy will silently become the implementation of choice for the
            duplicated strategy and the duplicates will be ignored.

    """
    StrategyFactory.load_strategies(test_for_uniqueness)


def create_strategy(
    strategy_type: "Union[StrategyType, str]", config: "StrategyConfig"
) -> "IStrategy":
    """Proxy function for `StrategyFactory.make_strategy()`.

    Parameters:
        strategy_type: A valid strategy type.
            See the [`StrategyType`][oteapi.plugins.factories.StrategyType] enumeration
            for a definition of valid strategy types.
        config: A strategy configuration.

    Raises:
        ValueError: If the `strategy_type` is not a valid strategy type.
            See the [`StrategyType`][oteapi.plugins.factories.StrategyType] enumeration
            for a definition of valid strategy types.

    Returns:
        The created strategy.

    """
    return StrategyFactory.make_strategy(config, strategy_type)


def create_download_strategy(config: "ResourceConfig") -> IDownloadStrategy:
    """Helper function to simplify creating a download strategy.

    Parameters:
        config: A download strategy configuration.

    Returns:
        The created download strategy.

    """
    strategy = StrategyFactory.make_strategy(config, StrategyType.DOWNLOAD)
    if not isinstance(strategy, IDownloadStrategy):
        raise TypeError(
            "Got back unexpected type from `StrategyFactory.make_strategy`. "
            "Expected a download strategy."
        )
    return strategy


def create_filter_strategy(config: "FilterConfig") -> IFilterStrategy:
    """Helper function to simplify creating a filter strategy.

    Parameters:
        config: A filter strategy configuration.

    Returns:
        The created filter strategy.

    """
    strategy = StrategyFactory.make_strategy(config, StrategyType.FILTER)
    if not isinstance(strategy, IFilterStrategy):
        raise TypeError(
            "Got back unexpected type from `StrategyFactory.make_strategy`. "
            "Expected a filter strategy."
        )
    return strategy


def create_mapping_strategy(config: "MappingConfig") -> IMappingStrategy:
    """Helper function to simplify creating a filter strategy.

    Parameters:
        config: A mapping strategy configuration.

    Returns:
        The created mapping strategy.

    """
    strategy = StrategyFactory.make_strategy(config, StrategyType.MAPPING)
    if not isinstance(strategy, IMappingStrategy):
        raise TypeError(
            "Got back unexpected type from `StrategyFactory.make_strategy`. "
            "Expected a mapping strategy."
        )
    return strategy


def create_parse_strategy(config: "ResourceConfig") -> IParseStrategy:
    """Helper function to simplify creating a parse strategy.

    Parameters:
        config: A parse strategy configuration.

    Returns:
        The created parse strategy.

    """
    strategy = StrategyFactory.make_strategy(config, StrategyType.PARSE)
    if not isinstance(strategy, IParseStrategy):
        raise TypeError(
            "Got back unexpected type from `StrategyFactory.make_strategy`. "
            "Expected a parse strategy."
        )
    return strategy


def create_resource_strategy(config: "ResourceConfig") -> IResourceStrategy:
    """Helper function to instanciate a resource strategy.

    Parameters:
        config: A resource strategy configuration.

    Returns:
        The created resource strategy.

    """
    strategy = StrategyFactory.make_strategy(config, StrategyType.RESOURCE)
    if not isinstance(strategy, IResourceStrategy):
        raise TypeError(
            "Got back unexpected type from `StrategyFactory.make_strategy`. "
            "Expected a resource strategy."
        )
    return strategy


def create_transformation_strategy(
    config: "TransformationConfig",
) -> ITransformationStrategy:
    """Helper function to instanciate a transformation strategy.

    Parameters:
        config: A transformation strategy configuration.

    Returns:
        The created transformation strategy.

    """
    strategy = StrategyFactory.make_strategy(config, StrategyType.TRANSFORMATION)
    if not isinstance(strategy, ITransformationStrategy):
        raise TypeError(
            "Got back unexpected type from `StrategyFactory.make_strategy`. "
            "Expected a transformation strategy."
        )
    return strategy

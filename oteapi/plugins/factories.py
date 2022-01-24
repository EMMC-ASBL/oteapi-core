"""Factory class for registering and creating strategy instances.

Factory wrapper methods for creating the individual strategies.
"""
from enum import Enum
from functools import lru_cache
from typing import TYPE_CHECKING

from oteapi.interfaces import (
    IDownloadStrategy,
    IFilterStrategy,
    IMappingStrategy,
    IParseStrategy,
    IResourceStrategy,
    ITransformationStrategy,
)

if TYPE_CHECKING:
    from typing import Any, Callable, Dict, Optional, Tuple, Type, Union
    from uuid import UUID

    from pydantic import AnyUrl

    from oteapi.interfaces import IStrategy
    from oteapi.models import (
        FilterConfig,
        MappingConfig,
        ResourceConfig,
        StrategyConfig,
        TransformationConfig,
    )

    ValueType = Union[int, str, AnyUrl, UUID]


class StrategyType(Enum):
    """An enumeration of available strategy types.

    Available strategy types:

    - download
    - filter
    - mapping
    - parse
    - resource
    - transformation

    """

    DOWNLOAD = "download"
    FILTER = "filter"
    MAPPING = "mapping"
    PARSE = "parse"
    RESOURCE = "resource"
    TRANSFORMATION = "transformation"

    @lru_cache
    def map_to_field(self) -> str:
        """Map strategy type to
        [`make_strategy()`][oteapi.plugins.factories.StrategyFactory.make_strategy]
        field value."""
        return {
            "download": "scheme",
            "filter": "filterType",
            "mapping": "mappingType",
            "parse": "mediaType",
            "resource": "accessService",
            "transformation": "transformation_type",
        }[self.value]

    @lru_cache
    def get_make_strategy_kwargs(self, config: "StrategyConfig") -> "Dict[str, Any]":
        """Get `make_strategy` kwargs.

        Parameters:
            config: A strategy configuration.

        Returns:
            The expected
            [`make_strategy()`][oteapi.plugins.factories.StrategyFactory.make_strategy]
            key-word-arguments (kwargs), meaning either a `field` or `index` key with
            an appropriate value.

        """
        if self.value == "download":
            # index
            return {
                "index": (
                    "scheme",
                    config.downloadUrl.scheme if config.downloadUrl is not None else "",
                )
            }

        # field
        return {"field": self.map_to_field()}


class StrategyFactory:
    """Decorator-based Factory class.

    Attributes:
        strategy_create_func: A local cache of all registerred strategies with their
            accompanying class.

    """

    strategy_create_func: "Dict[Tuple[str, ValueType], Type[IStrategy]]" = {}

    @classmethod
    def make_strategy(
        cls,
        model: "StrategyConfig",
        field: "Optional[str]" = None,
        index: "Optional[Tuple[str, ValueType]]" = None,
    ) -> "IStrategy":
        """Instantiate a strategy in a context class.

        Parameters:
            model: A strategy configuration.
            field: The strategy index type, e.g., `"scheme"`, `"mediaType"` or similar.
            index: A tuple of the `field` and a unique strategy name for the strategy
                index type/`field`.

        Returns:
            An instantiated strategy. The strategy is instantiated with the provided
            configuration, through the `model` parameter.

        """

        try:
            if not index and field:
                index = (field, model.dict()[field])
            elif not index:
                raise ValueError("field or index must be specified.")
            retval = cls.strategy_create_func[index]
        except KeyError as err:
            raise NotImplementedError(f"{index=!r} does not exist") from err
        return retval(model)

    @classmethod
    def register(
        cls, *args: "Tuple[str, ValueType]"
    ) -> "Callable[[Any], Type[IStrategy]]":
        """Register a strategy.

        The identifier for the strategy is defined by a set of key-value tuple pairs.
        """

        def decorator(strategy_class: "Type[IStrategy]") -> "Type[IStrategy]":
            for index in args:
                if index not in cls.strategy_create_func:
                    print(f"Registering {strategy_class.__name__} with {index}")
                    cls.strategy_create_func[index] = strategy_class
                else:
                    raise KeyError(f"{index=!r} is already registered.")
            return strategy_class

        return decorator

    @classmethod
    def unregister(cls, *args: "Tuple[str, ValueType]") -> None:
        """Unregister a strategy."""
        for index in args:
            cls.strategy_create_func.pop(index, None)


def create_strategy(
    strategy_type: "Union[StrategyType, str]", config: "StrategyConfig"
) -> "IStrategy":
    """General helper function to simplify creating any strategy.

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
    strategy_type = StrategyType(strategy_type)
    strategy_kwargs = strategy_type.get_make_strategy_kwargs()
    return StrategyFactory.make_strategy(model=config, **strategy_kwargs)


def create_download_strategy(config: "ResourceConfig") -> IDownloadStrategy:
    """Helper function to simplify creating a download strategy.

    Parameters:
        config: A download strategy configuration.

    Returns:
        The created download strategy.

    """
    strategy = StrategyFactory.make_strategy(
        config,
        index=(
            "scheme",
            config.downloadUrl.scheme if config.downloadUrl is not None else "",
        ),
    )
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
    strategy = StrategyFactory.make_strategy(config, field="filterType")
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
    strategy = StrategyFactory.make_strategy(config, field="mappingType")
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
    strategy = StrategyFactory.make_strategy(config, field="mediaType")
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
    strategy = StrategyFactory.make_strategy(config, field="accessService")
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
    strategy = StrategyFactory.make_strategy(config, field="transformation_type")
    if not isinstance(strategy, ITransformationStrategy):
        raise TypeError(
            "Got back unexpected type from `StrategyFactory.make_strategy`. "
            "Expected a transformation strategy."
        )
    return strategy

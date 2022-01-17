"""
Factory class for registering and creating strategy instances
"""
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Tuple, TypeVar
    from uuid import UUID

    from pydantic import AnyUrl, BaseModel

    from oteapi.models import (
        DownloadConfig,
        FilterConfig,
        MappingConfig,
        ResourceConfig,
        TransformationConfig,
    )
    from oteapi.interfaces import (
        IDownloadStrategy,
        IFilterStrategy,
        IMappingStrategy,
        IParseStrategy,
        IResourceStrategy,
        ITransformationStrategy,
    )

    ValueType = TypeVar("ValueType", int, str, AnyUrl, UUID)


class StrategyFactory:
    """
    Decorator based Factory class
    """

    strategy_create_func = {}

    @classmethod
    def make_strategy(cls, model: "BaseModel", field: str = None, index=None) -> "BaseModel":
        """Instanciate a strategy in a context class"""

        try:
            if not index and field:
                index = (field, model.dict()[field])
            retval = cls.strategy_create_func[index]
        except KeyError as err:
            raise NotImplementedError(f" {index=} doesn't exist") from err
        return retval(model)

    @classmethod
    def register(cls, *args: "Tuple[str, ValueType]"):
        """Register a strategy.

        The identifyer for the strategy is defined by a set of key-value tuple pairs.
        """

        def decorator(strategy_class):
            for index in args:
                if index not in cls.strategy_create_func:
                    print(f"Registering {strategy_class.__name__} with {index}")
                    cls.strategy_create_func[index] = strategy_class
                else:
                    raise KeyError(f" {index=} already registered")
            return strategy_class

        return decorator

    @classmethod
    def unregister(cls, *kwargs: "Tuple[str, ValueType]") -> None:
        """Unregister a strategy"""
        for index in kwargs:
            cls.strategy_create_func.pop(index, None)


def create_download_strategy(resource_config: "DownloadConfig") -> "IDownloadStrategy":
    """Helper function to simplify creating a download strategy"""
    return StrategyFactory.make_strategy(
        resource_config, index=("scheme", resource_config.downloadUrl.scheme)
    )


def create_filter_strategy(filter_config: "FilterConfig") -> "IFilterStrategy":
    """Helper function to simplify creating a filter strategy"""
    return StrategyFactory.make_strategy(filter_config, "filterType")


def create_transformation_strategy(
    transformation_config: "TransformationConfig",
) -> "ITransformationStrategy":
    """Helper function to instanciate a transformation strategy"""
    return StrategyFactory.make_strategy(transformation_config, "transformation_type")


def create_parse_strategy(resource_config: "ResourceConfig") -> "IParseStrategy":
    """Helper function to simplify creating a parse strategy"""
    return StrategyFactory.make_strategy(resource_config, field="mediaType")


def create_resource_strategy(resource_config: "ResourceConfig") -> "IResourceStrategy":
    """Helper function to instanciate a resource strategy"""
    return StrategyFactory.make_strategy(resource_config, "accessService")


def create_mapping_strategy(mapping_config: "MappingConfig") -> "IMappingStrategy":
    """Helper function to simplify creating a filter strategy"""
    return StrategyFactory.make_strategy(mapping_config, "mappingType")

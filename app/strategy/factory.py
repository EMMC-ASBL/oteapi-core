"""
Factory class for registering and creating strategy instances
"""
from typing import Tuple, TypeVar
from uuid import UUID

from pydantic import AnyUrl, BaseModel

ValueType = TypeVar("ValueType", int, str, AnyUrl, UUID)


class StrategyFactory:
    """
    Decorator based Factory class
    """

    strategy_create_func = {}

    @classmethod
    def make_strategy(cls, model: BaseModel, field: str = None, index=None):
        """Instanciate a strategy in a context class"""

        try:
            if not index and field:
                index = (field, model.dict()[field])
            retval = cls.strategy_create_func[index]
        except KeyError as err:
            raise NotImplementedError(f" {index=} doesn't exist") from err
        return retval(model)

    @classmethod
    def register(cls, *kwargs: Tuple[str, ValueType]):
        """Register a strategy. The identifyer for the strategy
        is defined by a set of key-value tuple pair.
        """

        def decorator(strategy_class):
            for index in kwargs:
                if index not in cls.strategy_create_func:
                    print(f"Registering {strategy_class.__name__} with {index}")
                    cls.strategy_create_func[index] = strategy_class
                else:
                    raise KeyError(f" {index=} already registered")
            return strategy_class

        return decorator

    @classmethod
    def unregister(cls, *kwargs: Tuple[str, ValueType]):
        """Unregister a strategy"""
        for index in kwargs:
            cls.strategy_create_func.pop(index, None)

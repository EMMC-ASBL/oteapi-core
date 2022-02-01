"""Generic data model for configuration attributes."""
from typing import Any, Optional

from pydantic import BaseModel, Field


class AttrDict(BaseModel):
    """An object whose attributes can also be accessed through
    subscription, like with a dictionary."""

    class Config:
        """Class for configuration of pydantic models."""

        extra = "allow"

    def __contains__(self, name: Any) -> bool:
        """Enable using the 'in' operator on this object."""
        return self.__dict__.__contains__(name)

    def __delitem__(self, key: str) -> None:
        """Enable deletion access through subscription."""
        if key in dir(self):
            self.__delattr__(key)
        else:
            raise KeyError(key)

    def __getitem__(self, key: str) -> Any:
        """Enable read access through subscription."""
        if key in dir(self):
            return getattr(self, key)
        raise KeyError(key)

    def __setitem__(self, key: str, value: Any) -> None:
        """Enable write access through subscription."""
        if key in self.__dict__:
            target_type = type(self.__dict__[key])
            if not isinstance(value, target_type):
                raise TypeError(
                    "Mapped value must be subclass of " + target_type.__name__
                )
        self.__dict__[key] = value


class GenericConfig(AttrDict):
    """Generic class for configuration objects."""

    configuration: Optional[AttrDict] = Field(
        None,
        description="Model-specific configuration options which can either "
        "be given as key/value-pairs or set as attributes.",
    )

    description: str = Field(
        __doc__,
        description="A description of the configuration model.",
    )

    @classmethod
    def __init_subclass__(cls) -> None:
        cls.__fields__["description"].default = cls.__doc__

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
            del self.__fields__[key]
            self.__fields_set__.remove(key)  # pylint: disable=no-member
        else:
            raise KeyError(key)

    def __getitem__(self, key: str) -> Any:
        """Enable read access through subscription."""
        if key in dir(self):
            return getattr(self, key)
        raise KeyError(key)

    def __setattr__(self, name: str, value: Any) -> None:
        """Extend BaseModel.__setattr__ with type-checking."""
        if name in self.__dict__ and self.__dict__[name]:
            target_type = type(self.__dict__[name])
            if not isinstance(value, target_type):
                raise TypeError(
                    "Mapped value must be subclass of " + target_type.__name__
                )
        super().__setattr__(name, value)

    def __setitem__(self, key: str, value: Any) -> None:
        """Enable write access through subscription."""
        self.__setattr__(key, value)

    def __len__(self):
        """Return number of items."""
        return self.__dict__.__len__()

    def __iter__(self):
        """Enable **unpacking."""
        return self.__dict__.__iter__()

    def items(self):
        """Return a view of all (key, value) pairs."""
        return self.__dict__.items()

    def keys(self):
        """Return a view of all keys."""
        return self.__dict__.keys()

    def values(self):
        """Return a view of all values."""
        return self.__dict__.values()

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        """Mapping `get`-method."""
        return self.__dict__.get(key, default)

    def __ne__(self, other: Any) -> bool:
        if isinstance(other, BaseModel):
            return self.dict() != other.dict()
        return self.dict() != other


class GenericConfig(BaseModel):
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
        """Initialize subclass descriptions with their docstrings."""
        cls.__fields__["description"].default = cls.__doc__

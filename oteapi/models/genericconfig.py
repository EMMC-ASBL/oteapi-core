"""Generic data model for configuration attributes."""
from typing import TYPE_CHECKING, Iterable, Mapping, MutableMapping

from pydantic import BaseModel, ConfigDict, Field
from pydantic.fields import PydanticUndefined

if TYPE_CHECKING:  # pragma: no cover
    from typing import Any, Optional, Tuple, Union


class AttrDict(BaseModel, MutableMapping):
    """An object whose attributes can also be accessed through
    subscription, like with a dictionary."""

    model_config = ConfigDict(
        extra="allow", validate_assignment=True, arbitrary_types_allowed=True
    )

    # Collection methods
    def __contains__(self, key: object) -> bool:
        """Mapping `__contains__`-method."""
        if not isinstance(key, str):
            raise TypeError(f"Keys must be of type `str`, not `{type(key).__name__}`.")
        return hasattr(self, key)

    def __len__(self) -> int:
        return len(self.model_dump())

    # Mapping methods
    def __getitem__(self, key: "Any") -> "Any":
        """Mapping `__getitem__`-method."""
        if not isinstance(key, str):
            raise TypeError(f"Keys must be of type `str`, not `{type(key).__name__}`.")
        try:
            return getattr(self, key)
        except AttributeError as exc:
            raise KeyError(key) from exc

    def items(self):
        """Return a view of all (key, value) pairs."""
        return self.model_dump().items()

    def keys(self):
        """Return a view of all keys."""
        return self.model_dump().keys()

    def values(self):
        """Return a view of all values."""
        return self.model_dump().values()

    def get(self, key: str, default: "Optional[Any]" = None) -> "Any":
        """Mapping `get`-method."""
        return getattr(self, key, default)

    def __eq__(self, value: object) -> bool:
        if isinstance(value, Mapping):
            return self.model_dump() == value
        if isinstance(value, BaseModel):
            return BaseModel.__eq__(self, value)
        return False

    # MutableMapping methods
    def __setitem__(self, key: "Any", value: "Any") -> None:
        """MutableMapping `__setitem__`-method."""
        if not isinstance(key, str):
            raise TypeError(f"Keys must be of type `str`, not `{type(key).__name__}`.")
        try:
            return self.__setattr__(key, value)
        except AttributeError as exc:
            raise KeyError(key) from exc

    def __delitem__(self, key: "Any") -> None:
        """MutableMapping `__delitem__`-method."""
        if not isinstance(key, str):
            raise TypeError(f"Keys must be of type `str`, not `{type(key).__name__}`.")
        try:
            return self.__delattr__(key)
        except AttributeError as exc:
            raise KeyError(key) from exc

    def clear(self) -> None:
        """MutableMapping `clear`-method."""
        for field in self.model_dump():
            del self[field]

    def update(  # type: ignore[override]
        self,
        other: "Optional[Union[Mapping[str, Any], Iterable[tuple[str, Any]]]]" = None,
        **kwargs,
    ) -> None:
        """MutableMapping `update`-method."""
        if other and isinstance(other, Mapping):
            for key, value in other.items():
                setattr(self, key, value)
        elif other and isinstance(other, BaseModel):
            for key, value in other:
                setattr(self, key, value)
        elif other and isinstance(other, Iterable):
            for entry in other:
                if not isinstance(entry, tuple):
                    raise TypeError(
                        "`other` must be an iterable of tuples of length two."
                    )
                if not len(entry) == 2:
                    raise ValueError(
                        "`other` must be an iterable of objects of length two."
                    )
            for key, value in other:  # type: ignore[misc]
                setattr(self, key, value)
        elif other:
            raise TypeError(
                "`other` must be of type `dict`, `Mapping`, `BaseModel` or "
                "`Iterable`, not `{type(other).__name__}`."
            )
        if kwargs:
            for key, value in kwargs.items():
                setattr(self, key, value)

    def pop(self, key: str, default: "Optional[Any]" = PydanticUndefined) -> "Any":
        """MutableMapping `pop`-method."""
        value = self.get(key, default)
        if value == PydanticUndefined:
            raise KeyError(key)
        if key in self:
            del self[key]
        return value

    def popitem(self) -> "Tuple[str, Any]":
        """MutableMapping `popitem`-method.

        Important:
            Unlike the regular `dict.popitem()` method, this one does _not_ respect
            LIFO (last-in, first-out).
            This is due to the fact that attributes are stored in a random order when
            initializing the model.

            However, it will respect LIFO with respect to the internal `model_fields`.

        """
        if not self:
            raise KeyError(f"popitem(): {self.__class__.__name__} is empty")

        key = list(self.keys())[-1]
        value = self.pop(key)
        return key, value


class GenericConfig(BaseModel):
    """Generic class for configuration objects."""

    configuration: AttrDict = Field(
        AttrDict(),
        description="Model-specific configuration options which can either "
        "be given as key/value-pairs or set as attributes.",
    )

    description: str = Field(
        __doc__,
        description="A description of the configuration model.",
    )

    @classmethod
    def __init_subclass__(cls, **kwargs) -> None:
        """Initialize subclass descriptions with their docstrings."""
        cls.model_fields["description"].default = cls.__doc__

    model_config = ConfigDict(validate_assignment=True, arbitrary_types_allowed=True)

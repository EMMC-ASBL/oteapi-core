"""Generic data model for configuration attributes."""
from typing import TYPE_CHECKING, Iterable, Mapping

from pydantic import BaseModel, Field
from pydantic.fields import Undefined

if TYPE_CHECKING:  # pragma: no cover
    from typing import Any, Optional, Tuple, Union


class AttrDict(BaseModel, Mapping):
    """An object whose attributes can also be accessed through
    subscription, like with a dictionary."""

    def __contains__(self, name: "Any") -> bool:
        """Enable using the 'in' operator on this object."""
        return self.__dict__.__contains__(name)

    def __delitem__(self, key: str) -> None:
        """Enable deletion access through subscription.

        If the item is a pydantic field, reset it and remove it from the set of set
        fields. Otherwise, delete the attribute.

        """
        if key in self.__dict__:
            if key in self.__fields__:
                # Reset field to default and remove from set of set fields
                setattr(self, key, self.__fields__[key].default)
                self.__fields_set__.remove(key)  # pylint: disable=no-member
            else:
                self.__delattr__(key)
        else:
            raise KeyError(key)

    def __getitem__(self, key: str) -> "Any":
        """Enable read access through subscription."""
        if key in self.__dict__:
            return getattr(self, key)
        raise KeyError(key)

    def __setitem__(self, key: str, value: "Any") -> None:
        """Enable write access through subscription."""
        setattr(self, key, value)

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

    def get(self, key: str, default: "Optional[Any]" = None) -> "Any":
        """Mapping `get`-method."""
        return self.__dict__.get(key, default)

    def __ne__(self, other: "Any") -> bool:
        """Implement the != operator."""
        if isinstance(other, BaseModel):
            return self.dict() != other.dict()
        return self.dict() != other

    def update(
        self, other: "Optional[Union[dict, AttrDict, Iterable[Any]]]" = None, **kwargs
    ) -> None:
        """MutableMapping `update`-method."""
        if other and isinstance(other, (dict, Mapping)):
            for key, value in other.items():
                setattr(self, key, value)
        elif other and isinstance(other, BaseModel):
            for key, value in other.dict().items():
                setattr(self, key, value)
        elif other and isinstance(other, Iterable):
            for entry in other:
                if not len(entry) == 2:
                    raise ValueError(
                        "`other` must be an iterable of objects of length two."
                    )
            for key, value in other:
                setattr(self, key, value)
        if kwargs:
            for key, value in kwargs.items():
                setattr(self, key, value)

    def pop(self, key: str, default: "Optional[Any]" = Undefined) -> "Any":
        """MutableMapping `pop`-method."""
        value = self.get(key, default)
        if value == Undefined:
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

            However, it will respect LIFO with respect to the internal `__dict__`.

        """
        if not self:
            raise KeyError(f"popitem(): {self.__class__.__name__} is empty")

        key = list(self.__dict__)[-1]
        value = self.pop(key)
        return key, value

    class Config:
        """Pydantic configuration for `AttrDict`.

        * **`extra`**
          Allow any attributes/fields to be defined - this is what makes this pydantic
          model an attribute dictionary.
        * **`validate_assignment`**
          Validate and cast set values.
          This is mainly relevant for sub-classes of `AttrDict`, where specific
          attributes have been defined.
        * **`arbitrary_types_allowed`**
          If a custom type is used for an attribute that doesn't have a `validate()`
          method, don't fail setting the attribute.

        """

        extra = "allow"
        validate_assignment = True
        arbitrary_types_allowed = True


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
    def __init_subclass__(cls) -> None:
        """Initialize subclass descriptions with their docstrings."""
        cls.__fields__["description"].default = cls.__doc__

    class Config:
        """Pydantic configuration for `GenericConfig`.

        * **`validate_assignment`**
          Validate and cast set values.
          This is mainly relevant for sub-classes of `AttrDict`, where specific
          attributes have been defined.
        * **`arbitrary_types_allowed`**
          If a custom type is used for an attribute that doesn't have a `validate()`
          method, don't fail setting the attribute.

        """

        validate_assignment = True
        arbitrary_types_allowed = True

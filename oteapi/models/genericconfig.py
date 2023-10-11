"""Generic data model for configuration attributes."""
import warnings
from collections.abc import Iterable, Mapping, MutableMapping
from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field
from pydantic.fields import PydanticUndefined

if TYPE_CHECKING:  # pragma: no cover
    from typing import Any, Optional, Tuple, Union


class AttrDict(BaseModel, MutableMapping):
    """An object whose attributes can also be accessed through
    subscription, like with a dictionary.

    Special pydantic configuration settings:

    - **`extra`**
      Allow any attributes/fields to be defined - this is what makes this pydantic
      model an attribute dictionary.
    - **`validate_assignment`**
      Validate and cast set values.
      This is mainly relevant for sub-classes of `AttrDict`, where specific
      attributes have been defined.
    - **`arbitrary_types_allowed`**
      If a custom type is used for an attribute that doesn't have a `validate()`
      method, don't fail setting the attribute.

    """

    model_config = ConfigDict(
        extra="allow", validate_assignment=True, arbitrary_types_allowed=True
    )

    # Collection methods
    def __contains__(self, key: object) -> bool:
        if not isinstance(key, str):
            raise TypeError(f"Keys must be of type `str`, not `{type(key).__name__}`.")
        return hasattr(self, key)

    def __len__(self) -> int:
        return len(self.model_dump())

    # Mapping methods
    def __getitem__(self, key: "Any") -> "Any":
        if not isinstance(key, str):
            raise TypeError(f"Keys must be of type `str`, not `{type(key).__name__}`.")
        try:
            return getattr(self, key)
        except AttributeError as exc:
            raise KeyError(key) from exc

    def items(self):
        return self.model_dump().items()

    def keys(self):
        return self.model_dump().keys()

    def values(self):
        return self.model_dump().values()

    def get(self, key: str, default: "Optional[Any]" = None) -> "Any":
        return getattr(self, key, default)

    def __eq__(self, value: object) -> bool:
        if isinstance(value, Mapping):
            return self.model_dump() == value
        if isinstance(value, BaseModel):
            return BaseModel.__eq__(self, value)
        return False

    # MutableMapping methods
    def __setitem__(self, key: "Any", value: "Any") -> None:
        if not isinstance(key, str):
            raise TypeError(f"Keys must be of type `str`, not `{type(key).__name__}`.")
        try:
            return self.__setattr__(key, value)
        except AttributeError as exc:
            raise KeyError(key) from exc

    def __delitem__(self, key: "Any") -> None:
        warnings.warn(
            "Item deletion used to reset fields to their default values. To keep using"
            " this functionality, use the `reset_field()` method.",
            DeprecationWarning,
        )

        if not isinstance(key, str):
            raise TypeError(f"Keys must be of type `str`, not `{type(key).__name__}`.")
        try:
            res = self.__delattr__(key)
        except AttributeError as exc:
            raise KeyError(key) from exc
        else:
            if key in self.model_fields_set:
                self.model_fields_set.remove(key)
            return res

    def clear(self) -> None:
        for field in self.model_dump():
            del self[field]

    def update(  # type: ignore[override]
        self,
        other: "Optional[Union[Mapping[str, Any], Iterable[tuple[str, Any]]]]" = None,
        **kwargs,
    ) -> None:
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

    def reset_field(self, field: str) -> None:
        """Reset a field to its default value.

        Warning:
            This will remove/delete a field that is not part of the model schema.

        Parameters:
            field: The field to reset.

        """
        if field not in self:
            raise KeyError(f"Field {field!r} does not exist.")

        if field in self.model_fields:
            # Part of the model schema
            schema_field = True

            # Set the field to its default value
            setattr(self, field, self.model_fields[field].default)
        else:
            # Not part of the model schema, but part of the extras
            schema_field = False

            # Remove the field altogether
            if self.model_extra is None:
                raise RuntimeError("Model has no extra fields.")

            try:
                self.model_extra.pop(field)
            except KeyError as exc:
                raise RuntimeError(
                    f"Field {field!r} can not be found in the model fields or extras."
                ) from exc

        # Remove it from fields set by the user
        if field in self.model_fields_set:
            self.model_fields_set.remove(field)

        # Check the field has been properly reset
        if schema_field:
            if field not in self:
                raise RuntimeError(f"Field {field!r} was not reset as expected.")
            if self[field] != self.model_fields[field].default:
                raise RuntimeError(
                    f"Field {field!r} was not reset to its default value as expected."
                )
        else:
            if field in self:
                raise RuntimeError(f"Field {field!r} was not removed as expected.")
        if field in self.model_fields_set:
            raise RuntimeError(
                f"Field {field!r} was not removed from the set of user-set fields as "
                "expected."
            )


class GenericConfig(BaseModel):
    """Generic class for configuration objects.

    Special pydantic configuration settings:

    - **`validate_assignment`**
      Validate and cast set values.
      This is mainly relevant for sub-classes of `AttrDict`, where specific
      attributes have been defined.
    - **`arbitrary_types_allowed`**
      If a custom type is used for an attribute that doesn't have a `validate()`
      method, don't fail setting the attribute.

    """

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

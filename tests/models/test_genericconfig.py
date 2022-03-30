"""Tests for `oteapi.models.genericconfig`"""
# pylint: disable=no-member
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from oteapi.models.genericconfig import GenericConfig


@pytest.fixture
def generic_config() -> "GenericConfig":
    """Return a usable `GenericConfig` for test purposes."""
    from pydantic import Field

    from oteapi.models.genericconfig import AttrDict, GenericConfig

    class CustomConfiguration(AttrDict):
        """A custom AttrDict class to use as `configuration` in CustomConfig."""

        string: str = Field("")

    class CustomConfig(GenericConfig):
        """A CustomConfig class."""

        configuration: CustomConfiguration = Field(
            CustomConfiguration(),
            description=GenericConfig.__fields__[
                "configuration"
            ].field_info.description,
        )

    return CustomConfig(
        configuration={
            "float": 3.14,
            "integer": 5,
            "string": "foo",
        }
    )


def test_subclass_description() -> None:
    """Test that the default description of the `configuration`
    attribute of a subclass of `GenericConfig` is the class docstring.
    """
    from oteapi.models.genericconfig import GenericConfig

    class SomeSubclass(GenericConfig):
        """This is a subclass of GenericConfig."""

    instance = SomeSubclass()
    assert instance.description == instance.__doc__


def test_attribute_get_item(generic_config: "GenericConfig") -> None:
    """Test configuration.__getitem__."""
    assert generic_config.configuration["integer"] == 5


def test_attribute_set(generic_config: "GenericConfig") -> None:
    """Test configuration.__setitem__, and thus also configuration.__setattr__.

    Assign different values to test dynamic type-casting.
    If a field has been specified to have a specific type, the incoming value should be
    cast to this type. However, if it is a non-specified type (similar to a standard
    dict key/value-pair), then it should be fine to change the value type for that
    given key.

    """
    generic_config.configuration["string"] = "bar"
    generic_config.configuration["string"] = 3.14
    assert generic_config.configuration["string"] == str(3.14)

    generic_config.configuration["float"] = "0"
    assert generic_config.configuration["float"] == "0"


def test_attribute_contains(generic_config: "GenericConfig") -> None:
    """Test confguration.__contains__."""
    assert "float" in generic_config.configuration


def test_attribute_del_item(generic_config: "GenericConfig") -> None:
    """Test configuration.__delitem__."""
    del generic_config.configuration["float"]
    assert "float" not in generic_config.configuration


def test_attrdict() -> None:
    """Test the behaviour of AttrDict."""
    from oteapi.models.genericconfig import AttrDict

    data = {"a": 1, "b": "foo", "c": "bar"}
    config = AttrDict(**data)
    assert config.a == config["a"] == config.get("a") == data["a"]
    assert config.b == config["b"] == config.get("b") == data["b"]

    assert {**config} == data


def test_attrdict_update() -> None:
    """Test supplying `AttrDict.update()` with different (valid) types."""
    from pydantic import Field

    from oteapi.models.genericconfig import AttrDict

    class SubAttrDict(AttrDict):
        """1st level sub-class of AttrDict."""

    class SubSubAttrDict(SubAttrDict):
        """2nd level sub-class of AttrDict."""

        test: SubAttrDict = Field(SubAttrDict())

    data = {"a": 1, "b": "foo", "c": "bar"}
    update_data = {"a": 2, "c": "bar", "d": "baz", "test": {"key": "value"}}
    final_data = data.copy()
    final_data.update(update_data)

    testing_types = (dict, AttrDict, SubAttrDict, SubSubAttrDict)
    for original_type in testing_types:
        for other_type in testing_types:
            original = original_type(**data)
            other = other_type(**update_data)
            original.update(other)
            assert {**original} == final_data


def test_attrdict_pop_popitem() -> None:
    """Test the `pop()` and `popitem()` methods for `AttrDict`."""
    from oteapi.models.genericconfig import AttrDict

    data = {"a": 1, "b": "foo", "c": "bar"}
    attrdict = AttrDict(**data)

    popped_value = attrdict.pop("b")
    assert popped_value == data["b"]
    assert len(attrdict) == len(data) - 1

    # Should follow LIFO (last-in, first-out) wrt `__dict__`
    attrdict_keys = list(attrdict.__dict__)
    last_entry = (attrdict_keys[-1], data[attrdict_keys[-1]])
    popped_item = attrdict.popitem()
    assert popped_item == last_entry
    assert len(attrdict) == len(data) - 2

    # Pop non-existing key with default value
    assert attrdict.pop("d", None) is None
    assert attrdict.pop("d", "some default value") == "some default value"

    # Pop non-existing key without default value - should raise KeyError
    with pytest.raises(KeyError, match=r"^'d'$"):
        attrdict.pop("d")

    # Only a single entry is left in attrdict, let's check
    attrdict_keys = list(attrdict.__dict__)
    last_entry = (attrdict_keys[-1], data[attrdict_keys[-1]])
    assert attrdict.popitem() == last_entry

    # Popitem - attrdict is empty, should raise KeyError
    with pytest.raises(KeyError, match=r"^'popitem\(\): .* is empty'$"):
        attrdict.popitem()

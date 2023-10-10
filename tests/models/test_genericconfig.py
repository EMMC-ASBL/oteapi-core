"""Tests for `oteapi.models.genericconfig`"""
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from oteapi.models.genericconfig import AttrDict, GenericConfig

    class CustomConfiguration(AttrDict):
        """A custom AttrDict class to use as `configuration` in CustomConfig."""

        string: str

    class CustomConfig(GenericConfig):
        """A CustomConfig class."""

        configuration: CustomConfiguration


@pytest.fixture
def generic_config() -> "CustomConfig":
    """Return a usable `CustomConfig` for test purposes."""
    from pydantic import Field

    from oteapi.models.genericconfig import AttrDict, GenericConfig

    class CustomConfiguration(AttrDict):
        """A custom AttrDict class to use as `configuration` in CustomConfig."""

        string: str = Field("")
        required_string: str = Field(...)

    class CustomConfig(GenericConfig):
        """A CustomConfig class."""

        configuration: CustomConfiguration = Field(
            CustomConfiguration(required_string=""),
            description=GenericConfig.model_fields["configuration"].description,
        )

    return CustomConfig(
        configuration={
            "float": 3.14,
            "integer": 5,
            "string": "foo",
            "required_string": "bar",
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


def test_attribute_get_item(generic_config: "CustomConfig") -> None:
    """Test configuration.__getitem__."""
    assert generic_config.configuration["integer"] == 5


def test_attribute_get_item_fail(generic_config: "CustomConfig") -> None:
    """Ensure KeyError is raised for a non-existent key."""
    non_existent_key = "non_existent_key"
    assert non_existent_key not in generic_config.configuration
    with pytest.raises(KeyError):
        generic_config.configuration[non_existent_key]


def test_attribute_set(generic_config: "CustomConfig") -> None:
    """Test configuration.__setitem__, and thus also configuration.__setattr__.

    Assign different values to test dynamic type-casting.
    If a field has been specified to have a specific type, the incoming value should be
    cast to this type. However, if it is a non-specified type (similar to a standard
    dict key/value-pair), then it should be fine to change the value type for that
    given key.

    NOTE: Pydantic v2 will not coerce all types, e.g. any type to `str`.
    One should instead use Annotated to create custom types.
    Example: generic_config.configuration["string"] = 3.14 will NOT result in
    generic_config.configuration["string"] == "3.14"
    See https://docs.pydantic.dev/latest/usage/types/custom/ for more information.
    UPDATE: As of v2.4 there's a new config setting that re-implements this behaviour:
    https://docs.pydantic.dev/latest/api/config/#pydantic.config.ConfigDict.coerce_numbers_to_str

    """
    from pydantic import ValidationError

    generic_config.configuration["string"] = "bar"

    with pytest.raises(ValidationError):
        # Not allowed to coerce a float to a string
        generic_config.configuration["string"] = 3.14

    assert generic_config.configuration["string"] == "bar"

    generic_config.configuration["float"] = "0"
    assert generic_config.configuration["float"] == "0"


def test_attribute_contains(generic_config: "CustomConfig") -> None:
    """Test confguration.__contains__."""
    assert "float" in generic_config.configuration


def test_attribute_del_item(generic_config: "CustomConfig") -> None:
    """Test configuration.__delitem__."""
    # "float" is not defined as a pydantic model field, i.e., it's not part of the
    # model schema, but rather the model extras.
    # This means it **should** be deleted from the model extras,
    # and it **should** be removed from the instance.
    assert "float" in generic_config.configuration.model_fields_set
    assert "float" not in generic_config.configuration.model_json_schema()["properties"]

    del generic_config.configuration["float"]

    assert "float" not in generic_config.configuration
    assert "float" not in generic_config.configuration.model_fields_set
    assert "float" not in generic_config.configuration.model_json_schema()["properties"]

    # "string" is defined as a pydantic model field, i.e., it's part of the model
    # schema.
    # This means it **should not** be deleted from the model schema,
    # but it **should** be removed from the model instance.
    generic_config.configuration["string"] = "my secret string"
    assert generic_config.configuration.string == "my secret string"
    assert (
        generic_config.configuration.string
        != generic_config.configuration.model_fields["string"].default
    )
    assert "string" in generic_config.configuration.model_fields_set
    assert "string" in generic_config.configuration.model_json_schema()["properties"]

    del generic_config.configuration["string"]

    assert "string" not in generic_config.configuration
    assert "string" in generic_config.configuration.model_json_schema()["properties"]


def test_attribute_reset_field(generic_config: "CustomConfig") -> None:
    """Test configuration.reset_field()."""
    # "float" is not defined as a pydantic model field, i.e., it's not part of the
    # model schema, but rather the model extras.
    # This means it **should** be deleted from the model extras,
    # and it **should** be removed from the instance.
    assert "float" in generic_config.configuration.model_fields_set
    assert "float" not in generic_config.configuration.model_json_schema()["properties"]

    generic_config.configuration.reset_field("float")

    assert "float" not in generic_config.configuration
    assert "float" not in generic_config.configuration.model_fields_set
    assert "float" not in generic_config.configuration.model_json_schema()["properties"]

    # "string" is defined as a pydantic model field, i.e., it's part of the model
    # schema.
    # This means it **should not** be deleted, but reset to its default value
    # and removed from the set of user-set fields.
    generic_config.configuration["string"] = "my secret string"
    assert generic_config.configuration.string == "my secret string"
    assert "string" in generic_config.configuration.model_fields_set

    generic_config.configuration.reset_field("string")

    assert "string" in generic_config.configuration
    assert (
        generic_config.configuration.string
        == generic_config.configuration.model_fields["string"].default
    )
    assert "string" not in generic_config.configuration.model_fields_set
    assert "string" in generic_config.configuration.model_json_schema()["properties"]


def test_attribute_del_item_fail(generic_config: "CustomConfig") -> None:
    """Ensure KeyError is raised if key does not exist in AttrDict."""
    non_existent_key = "non_existant_key"
    assert non_existent_key not in generic_config.configuration
    with pytest.raises(KeyError):
        del generic_config.configuration[non_existent_key]

    # Required fields can also be deleted
    del generic_config.configuration["required_string"]


def test_attribute_ne(generic_config: "CustomConfig") -> None:
    """Test configuration.__ne__()."""
    from pydantic import BaseModel

    class Test(BaseModel):
        """Test pydantic model."""

        test: str

    assert generic_config.configuration != Test(test="test")
    assert generic_config.configuration != {"test": "test"}
    assert generic_config.configuration != 2

    copy_config = generic_config.configuration.model_copy(deep=True)
    assert (generic_config.configuration != copy_config) is False


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
    from pydantic import BaseModel, ConfigDict, Field

    from oteapi.models.genericconfig import AttrDict

    class Foo(BaseModel):
        """Foo pydantic model."""

        model_config = ConfigDict(extra="allow")

    class SubAttrDict(AttrDict):
        """1st level sub-class of AttrDict."""

    class SubSubAttrDict(SubAttrDict):
        """2nd level sub-class of AttrDict."""

        test: SubAttrDict = Field(SubAttrDict())

    data = {"a": 1, "b": "foo", "c": "bar"}
    update_data = {"a": 2, "c": "bar", "d": "baz", "test": {"key": "value"}}
    final_data = data.copy()
    final_data.update(update_data)

    testing_types = dict, AttrDict, SubAttrDict, SubSubAttrDict
    non_update_method_testing_types = testing_types + (Foo, tuple, list)
    for original_type in testing_types:
        for other_type in non_update_method_testing_types:
            original = original_type(**data)
            try:
                other = other_type(**update_data)
            except TypeError:
                other = other_type(update_data.items())
            original.update(other)
            assert {**original} == final_data, (
                f"original type: {original_type.__name__}, "
                f"other type: {other_type.__name__}"
            )

    # Check TypeError is raised for invalid types
    with pytest.raises(TypeError, match=r".*must be of type.*"):
        AttrDict(**data).update(1)

    # Check TypeError is raised if inner Iterable type is not a tuple
    with pytest.raises(TypeError, match=r".*must be an iterable of tuples.*"):
        AttrDict(**data).update(list(list(_) for _ in update_data.items()))

    # Check ValueError is raised if inner Iterable type is not of length two
    with pytest.raises(
        ValueError, match=r".*must be an iterable of objects of length two.*"
    ):
        AttrDict(**data).update([("a", 1, 2)])


def test_attrdict_pop_popitem() -> None:
    """Test the `pop()` and `popitem()` methods for `AttrDict`."""
    from oteapi.models.genericconfig import AttrDict

    data = {"a": 1, "b": "foo", "c": "bar"}
    attrdict = AttrDict(**data)

    popped_value = attrdict.pop("b")
    assert popped_value == data["b"]
    assert len(attrdict) == len(data) - 1

    # Should follow LIFO (last-in, first-out) wrt standard dict behaviour
    attrdict_keys = list(attrdict.keys())
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
    attrdict_keys = list(attrdict.keys())
    last_entry = (attrdict_keys[-1], data[attrdict_keys[-1]])
    assert attrdict.popitem() == last_entry

    # Popitem - attrdict is empty, should raise KeyError
    with pytest.raises(KeyError, match=r"^'popitem\(\): .* is empty'$"):
        attrdict.popitem()


def test_attrdict_values() -> None:
    """Test the `values()` method for `AttrDict`."""
    from oteapi.models.genericconfig import AttrDict

    class SubAttrDict(AttrDict):
        """1st level sub-class of AttrDict."""

        test: str

    data = {"a": 1, "b": "foo", "c": "bar"}
    attrdict = AttrDict(**data)

    assert list(attrdict.values()) == list(data.values())

    # Check values return both model schema field values as well as model extra
    # field values
    subattrdict = SubAttrDict(test="test", **data)

    assert list(subattrdict.values()) == ["test"] + list(data.values())


def test_attrdict_clear() -> None:
    """Test the `clear()` method for `AttrDict`."""
    from oteapi.models.genericconfig import AttrDict

    data = {"a": 1, "b": "foo", "c": "bar"}
    attrdict = AttrDict(**data)

    assert len(attrdict) == len(data)
    assert len(attrdict.model_fields_set) == len(data)

    attrdict.clear()

    assert len(attrdict) == 0
    assert len(attrdict.model_fields_set) == 0

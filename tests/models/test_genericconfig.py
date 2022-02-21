"""Tests for `oteapi.models.genericconfig`"""
# pylint: disable=no-member
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from oteapi.models.genericconfig import GenericConfig


@pytest.fixture
def generic_config() -> "GenericConfig":
    """Return a usable `GenericConfig` for test purposes."""
    from oteapi.models.genericconfig import GenericConfig

    return GenericConfig(
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
    """Test configuration.__setitem__, and thus also
    configuration.__setattr__.

    Assign both a valid and an invalid value, to test dynamic
    type-checking.
    """
    generic_config.configuration["string"] = "bar"
    try:
        generic_config.configuration["string"] = 3.14
        assert False
    except TypeError:
        pass


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

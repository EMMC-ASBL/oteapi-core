"""Tests for `oteapi.models.genericconfig`"""
from oteapi.models.genericconfig import GenericConfig

generic_config = GenericConfig(
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

    class SomeSubclass(GenericConfig):
        """This is a subclass of GenericConfig."""

    instance = SomeSubclass()
    assert instance.description == instance.__doc__


def test_attribute_get_item() -> None:
    """Test configuration.__getitem__."""
    assert generic_config.configuration["integer"] == 5


def test_attribute_set() -> None:
    """Test configuration.__setitem__, and thus also
    configuration.__setattr__.
    """
    generic_config.configuration["string"] = "bar"
    # Test dynamic type checking
    try:
        generic_config.configuration["string"] = 3.14
        assert False
    except TypeError:
        pass


def test_attribute_contains() -> None:
    """Test confguration.__contains__."""
    assert "float" in generic_config.configuration


def test_attribute_del_item() -> None:
    """Test configuration.__delitem__."""
    del generic_config.configuration["float"]
    assert "float" not in generic_config.configuration

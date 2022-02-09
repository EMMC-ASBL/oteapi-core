"""Tests for `oteapi.models.genericconfig`"""
# pylint: disable=no-member


def test_attrdict() -> None:
    """Test the behaviour of AttrDict."""
    from oteapi.models.genericconfig import AttrDict

    data = {"a": 1, "b": "foo", "c": "bar"}
    config = AttrDict(**data)
    assert config.a == config["a"] == config.get("a") == data["a"]
    assert config.b == config["b"] == config.get("b") == data["b"]

    assert {**config} == data

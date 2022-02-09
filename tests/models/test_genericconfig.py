"""Tests for `oteapi.models.genericceconfig`"""
import pytest


def test_attrdict() -> None:
    """Test the behaviour of AttrDict."""
    from oteapi.models.genericconfig import AttrDict

    config = AttrDict(a=1, b='foo', c='bar')
    assert config.a == 1
    assert config.b == 'foo'

    assert **config == {'a': 1, 'b': 'foo', 'c': 'bar'}

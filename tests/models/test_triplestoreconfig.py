"""Tests for `oteapi.models.triplestoreconfig`"""

import pytest


def test_triplestoreconfig() -> None:
    """Pytest for TripleStoreConfig."""
    import json

    from oteapi.models.triplestoreconfig import TripleStoreConfig
    from oteapi.settings import settings

    description = """TripleStore Configuration.

    This is a configuration for the
    [`TripleStore`][oteapi.triplestore.triplestore.TripleStore].

    This class should not be used directly as a configuration object
    for a strategy object, but only as a configuration field inside
    a configuration object.
    """

    config = {
        "agraphHost": "localhost",
        "agraphPort": 8080,
        "user": "abc",
        "password": "pass",
        "repositoryName": "test",
    }
    config_invalid_1 = {
        "agraphHost": "localhost",
        "agraphPort": 8080,
        "password": "pass",
        "repositoryName": "test",
    }
    config_invalid_2 = {
        "agraphHost": "localhost",
        "agraphPort": 8080,
        "user": "abc",
        "repositoryName": "test",
    }
    config_hidden = {
        "user": "**********",
        "password": "**********",
        "configuration": {},
        "description": description,
        "repositoryName": "test",
        "agraphHost": "localhost",
        "agraphPort": 8080,
    }
    config_exposed = {
        "user": "abc",
        "password": "pass",
        "configuration": {},
        "description": description,
        "repositoryName": "test",
        "agraphHost": "localhost",
        "agraphPort": 8080,
    }

    # NOTE: model_dump_json() returns a compact JSON string (no extra spaces or
    #       newlines). To match its format, we use json.dumps() with indent=None and
    #       separators=(",", ":")

    settings.expose_secrets = False
    assert TripleStoreConfig(**config).model_dump_json() == json.dumps(
        config_hidden, indent=None, separators=(",", ":")
    )

    settings.expose_secrets = True
    assert TripleStoreConfig(**config).model_dump_json() == json.dumps(
        config_exposed, indent=None, separators=(",", ":")
    )

    for config in [config_invalid_1, config_invalid_2]:
        with pytest.raises(ValueError, match="User and password must be defined."):
            TripleStoreConfig(**config)

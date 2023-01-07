"""Tests for `oteapi.models.secretconfig`"""


def test_secretconfig():

    import os
    import json
    from oteapi.models.secretconfig import SecretConfig

    base_config = {"secret": "abc"}
    config_exposed = {
        "configuration": {},
        "description": "Simple model for handling secret in other config-models.",
        "user": None,
        "password": None,
        "secret": "abc",
        "client_id": None,
        "client_secret": None,
    }

    config = SecretConfig(**base_config)
    assert config.json() == json.dumps(config_exposed)

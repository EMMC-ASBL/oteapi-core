"""Tests for `oteapi.models.functionconfig`"""


def test_functionconfig():

    from oteapi.models.functionconfig import FunctionConfig
    import json

    base_config = {"functionType": "foo/bar", "secret": "abc"}
    config_exposed = {
        "configuration": {},
        "description": "Function Strategy Data Configuration.",
        "user": None,
        "password": None,
        "secret": "abc",
        "client_id": None,
        "client_secret": None,
        "functionType": "foo/bar",
    }

    config = FunctionConfig(**base_config)

    assert config.json() == json.dumps(config_exposed)

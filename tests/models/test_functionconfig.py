"""Tests for `oteapi.models.functionconfig`"""


def test_functionconfig() -> None:
    """Pytest for FunctionConfig, mainly for testing the included secrets."""
    import json

    from oteapi.models.functionconfig import FunctionConfig
    from oteapi.settings import settings

    base_config = {"functionType": "foo/bar", "token": "abc"}
    config_exposed = {
        "user": None,
        "password": None,
        "token": "abc",
        "client_id": None,
        "client_secret": None,
        "configuration": {},
        "description": "Function Strategy Data Configuration.",
        "functionType": "foo/bar",
    }

    config_hidden = {
        "user": None,
        "password": None,
        "token": "**********",
        "client_id": None,
        "client_secret": None,
        "configuration": {},
        "description": "Function Strategy Data Configuration.",
        "functionType": "foo/bar",
    }

    # NOTE: model_dump_json() returns a JSON string with no whitespace.
    #       This is why we use json.dumps() with indent=None and separators=(",", ":")

    settings.expose_secrets = False
    assert FunctionConfig(**base_config).model_dump_json() == json.dumps(
        config_hidden, indent=None, separators=(",", ":")
    )

    settings.expose_secrets = True
    assert FunctionConfig(**base_config).model_dump_json() == json.dumps(
        config_exposed, indent=None, separators=(",", ":")
    )

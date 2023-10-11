"""Tests for `oteapi.models.secretconfig`"""


def test_secretconfig():
    """Pytest for SecretConfig."""
    import json

    from oteapi.models.secretconfig import SecretConfig
    from oteapi.settings import settings

    base_config = {"token": "abc"}
    config_exposed = {
        "user": None,
        "password": None,
        "token": "abc",
        "client_id": None,
        "client_secret": None,
    }

    config_hidden = {
        "user": None,
        "password": None,
        "token": "**********",
        "client_id": None,
        "client_secret": None,
    }

    # NOTE: model_dump_json() returns a compact JSON string (no extra spaces or
    #       newlines). To match its format, we use json.dumps() with indent=None and
    #       separators=(",", ":")

    settings.expose_secrets = False
    assert SecretConfig(**base_config).model_dump_json() == json.dumps(
        config_hidden, indent=None, separators=(",", ":")
    )

    settings.expose_secrets = True
    assert SecretConfig(**base_config).model_dump_json() == json.dumps(
        config_exposed, indent=None, separators=(",", ":")
    )

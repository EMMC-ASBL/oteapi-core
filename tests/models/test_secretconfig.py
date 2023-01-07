"""Tests for `oteapi.models.secretconfig`"""


def test_secretconfig():
    """Pytest for SecretConfig."""
    import json

    from oteapi.models.secretconfig import SecretConfig
    from oteapi.settings import settings

    base_config = {"secret": "abc"}
    config_exposed = {
        "user": None,
        "password": None,
        "secret": "abc",
        "client_id": None,
        "client_secret": None,
    }

    config_hidden = {
        "user": None,
        "password": None,
        "secret": "**********",
        "client_id": None,
        "client_secret": None,
    }

    settings.expose_secrets = False
    assert SecretConfig(**base_config).json() == json.dumps(config_hidden)

    settings.expose_secrets = True
    assert SecretConfig(**base_config).json() == json.dumps(config_exposed)

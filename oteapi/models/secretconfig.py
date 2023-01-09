"""AttrDict for specifying user credentials or secrets."""

import json
from typing import Optional

from pydantic import Field, SecretStr

from oteapi.models.genericconfig import AttrDict
from oteapi.settings import settings


def json_dumps(model, *, default):
    """Alternative function for dumping exposed
    secrets to json when model is serialized."""
    return json.dumps(
        {
            key: (
                value.get_secret_value()
                if settings.expose_secrets and isinstance(value, SecretStr)
                else value
            )
            for key, value in model.items()
        },
        default=default,
    )


class SecretConfig(AttrDict):
    """Simple model for handling secret in other config-models."""

    user: Optional[SecretStr] = Field(None, description="User name for authentication.")
    password: Optional[SecretStr] = Field(
        None, description="Password for authentication."
    )
    token: Optional[SecretStr] = Field(
        None,
        description="An access token for providing access and meta data to an application.",
    )
    client_id: Optional[SecretStr] = Field(
        None, description="Client ID for an OAUTH2 client."
    )
    client_secret: Optional[SecretStr] = Field(
        None, description="Client secret for an OAUTH2 client."
    )

    class Config:
        """Pydantic donfiguration for SecretConfig when serialized or exported."""

        # json_encoders = {
        #     SecretStr: lambda secret: (
        #         secret.get_secret_value()
        #         if settings.expose_secrets and secret
        #         else secret
        #     )
        # }
        #
        # Using the json_encoders directly throws an
        # `ValueError: Circular reference detected` when
        # the model is called via the json-method, but ONLY
        # if the `settings.expose_secrets` is used. Why?
        # There are no schema-dependencies between the settings
        # and the SecretConfig and calling `forward_update_refs`
        # does not make any change.
        # Alternatively, `json_dumps` (see below) can
        # be called without any exception.

        json_dumps = json_dumps

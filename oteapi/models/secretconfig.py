"""AttrDict for specifying user credentials or secrets."""
from typing import Annotated, Optional

from pydantic import BaseModel, Field, PlainSerializer, SecretStr

from oteapi.settings import settings

TogglableSecretStr = Annotated[
    SecretStr,
    PlainSerializer(
        lambda value: value.get_secret_value()
        if settings.expose_secrets
        else str(value),
        return_type=str,
        when_used="json-unless-none",
    ),
]
"""Annotated type alias for a secret string that can be toggled to be exposed or not."""


class SecretConfig(BaseModel):
    """Simple model for handling secret in other config-models."""

    user: Optional[TogglableSecretStr] = Field(
        None, description="User name for authentication."
    )
    password: Optional[TogglableSecretStr] = Field(
        None, description="Password for authentication."
    )
    token: Optional[TogglableSecretStr] = Field(
        None,
        description=(
            "An access token for providing access and meta data to an application."
        ),
    )
    client_id: Optional[TogglableSecretStr] = Field(
        None, description="Client ID for an OAUTH2 client."
    )
    client_secret: Optional[TogglableSecretStr] = Field(
        None, description="Client secret for an OAUTH2 client."
    )

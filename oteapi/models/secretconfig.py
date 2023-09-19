"""AttrDict for specifying user credentials or secrets."""
from typing import Optional

from pydantic import BaseModel, Field, SecretStr, field_serializer

from oteapi.settings import settings


class SecretConfig(BaseModel):
    """Simple model for handling secret in other config-models."""

    user: Optional[SecretStr] = Field(None, description="User name for authentication.")
    password: Optional[SecretStr] = Field(
        None, description="Password for authentication."
    )
    token: Optional[SecretStr] = Field(
        None,
        description=(
            "An access token for providing access and meta data to an application."
        ),
    )
    client_id: Optional[SecretStr] = Field(
        None, description="Client ID for an OAUTH2 client."
    )
    client_secret: Optional[SecretStr] = Field(
        None, description="Client secret for an OAUTH2 client."
    )

    @field_serializer(
        "user",
        "password",
        "token",
        "client_id",
        "client_secret",
        when_used="json-unless-none",
    )
    def serialize_secrets(self, value: SecretStr, _) -> str:
        """Convert secret values to strings if expose_secrets=True in settings."""
        return value.get_secret_value() if settings.expose_secrets else str(value)

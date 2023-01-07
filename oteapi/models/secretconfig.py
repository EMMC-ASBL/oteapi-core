"""AttrDict for specifying user credentials or secrets."""

from typing import TYPE_CHECKING, Optional

from pydantic import Field, SecretStr, root_validator
from oteapi.models.genericconfig import GenericConfig
from oteapi.utils.json_encoders import encode_secrets

if TYPE_CHECKING:  # pragma: no cover
    from typing import Any, Dict


class SecretConfig(GenericConfig):
    """Simple model for handling secret in other config-models."""

    user: Optional[SecretStr] = Field(None, description="User name for authentication.")
    password: Optional[SecretStr] = Field(
        None, description="Password for authentication."
    )
    secret: Optional[SecretStr] = Field(
        None,
        description="A secret passed to the config, e.g. an access token.",
    )
    client_id: Optional[SecretStr] = Field(None, description="Client ID for an OAUTH2 client")
    client_secret: Optional[SecretStr] = Field(None, description="Client secret for an OAUTH2 client")

    class Config:
        json_encoders = {SecretStr: encode_secrets}

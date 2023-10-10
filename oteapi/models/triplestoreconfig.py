"""Pydantic TripleStore Configuration Data Model."""
from typing import Annotated, Optional

from pydantic import Field, model_validator

from oteapi.models.genericconfig import GenericConfig
from oteapi.models.secretconfig import SecretConfig, TogglableSecretStr

ExcludeTogglableSecretStr = Annotated[Optional[TogglableSecretStr], Field(exclude=True)]
"""Annotated type alias for excluding a togglable secret from serialization."""


class TripleStoreConfig(GenericConfig, SecretConfig):
    """TripleStore Configuration.

    This is a configuration for the
    [`TripleStore`][oteapi.triplestore.triplestore.TripleStore].

    This class should not be used directly as a configuration object
    for a strategy object, but only as a configuration field inside
    a configuration object.
    """

    repositoryName: str = Field(
        ..., description="The repository name, where the mappings are stored."
    )
    agraphHost: str = Field(..., description="AllegroGraph host name.")
    agraphPort: int = Field(..., description="AllegroGraph port number.")

    # Exclude these inherited fields from serialization
    token: Annotated[
        ExcludeTogglableSecretStr, SecretConfig.model_fields["token"]
    ] = SecretConfig.model_fields["token"].default
    client_id: Annotated[
        ExcludeTogglableSecretStr, SecretConfig.model_fields["client_id"]
    ] = SecretConfig.model_fields["client_id"].default
    client_secret: Annotated[
        ExcludeTogglableSecretStr, SecretConfig.model_fields["client_secret"]
    ] = SecretConfig.model_fields["client_secret"].default

    @model_validator(mode="after")
    def ensure_user_pass(self) -> "TripleStoreConfig":
        """Ensure that user/password are set, since they are optional in the
        SecretConfig."""
        if not all(getattr(self, _) for _ in ["user", "password"]):
            raise ValueError("User and password must be defined.")
        return self

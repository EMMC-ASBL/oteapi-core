"""Pydantic TripleStore Configuration Data Model."""
from pydantic import Field, model_validator

from oteapi.models.genericconfig import GenericConfig
from oteapi.models.secretconfig import SecretConfig


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

    @model_validator(mode="after")
    def ensure_user_pass(self) -> "TripleStoreConfig":
        """Ensure that user/password are set, since they are optional in the
        SecretConfig."""
        if not all(getattr(self, _) for _ in ["user", "password"]):
            raise ValueError("User and password must be defined.")
        return self

"""Pydantic TripleStore Configuration Data Model."""
from typing import TYPE_CHECKING

from pydantic import Field, root_validator

from oteapi.models.genericconfig import GenericConfig
from oteapi.models.secretconfig import SecretConfig

if TYPE_CHECKING:  # pragma: no cover
    from typing import Any, Dict


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
    agraphHost: str = Field(
        ...,
        description="AllegroGraph host name.",
    )
    agraphPort: int = Field(
        ...,
        description="AllegroGraph port number.",
    )

    @root_validator
    def ensure_user_pass(cls, values: "Dict[str, Any]") -> "Dict[str, Any]":
        """Ensure that user/password are set, since they are optional in the
        SecretConfig."""
        if not all(values.get(_) for _ in ["user", "password"]):
            raise ValueError("User and password must be defined.")
        return values

    class Config:
        """Pydantic configuration for TripleStoreConfig."""

        fields = {
            "token": {"exclude": True},
            "client_id": {"exclude": True},
            "client_secret": {"exclude": True},
        }
        """The `fields`-config enables that `token`, `client_id` and `client_secret`
        will be excluded, when the model is serialized."""

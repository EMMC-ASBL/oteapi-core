"""Pydantic TripleStore Configuration Data Model."""
from pydantic import Field, SecretStr

from oteapi.models.genericconfig import AttrDict


class TripleStoreConfig(AttrDict):
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
    agraphUser: str = Field(
        ...,
        description="AllegroGraph user name.",
    )
    agraphPassword: SecretStr = Field(
        ...,
        description="AllegroGraph user password.",
    )

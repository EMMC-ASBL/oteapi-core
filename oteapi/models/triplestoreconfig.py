"""Pydantic TripleStore Configuration Data Model."""
from pydantic import Field

from oteapi.models.genericconfig import AttrDict


class TripleStoreConfig(AttrDict):
    """TripleStore Configuration.

    This class should not be used directly as a configuration object
    for a strategy object, but only as a configuration field inside
    a configuration object.
    """

    repositoryName: str = Field(
        ..., description="repository name where the mappings need to be stored."
    )
    agraphHost: str = Field(
        ...,
        description="Allegrograph host name to make connection to the triplestore.",
    )
    agraphPort: int = Field(
        ...,
        description="Allegrograph port number to make connection to the triplestore.",
    )
    agraphUser: str = Field(
        ...,
        description="Allegrograph user name to login to the triplestore.",
    )
    agraphPassword: str = Field(
        ...,
        description="Allegrograph password to login to the triplestore.",
    )

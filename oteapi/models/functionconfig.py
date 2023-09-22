"""Pydantic Function Configuration Data Model."""
from oteapi.models.genericconfig import GenericConfig
from oteapi.models.secretconfig import SecretConfig
from oteapi.utils._pydantic import Field


class FunctionConfig(GenericConfig, SecretConfig):
    """Function Strategy Data Configuration."""

    functionType: str = Field(
        ...,
        description=("Type of registered function strategy."),
    )

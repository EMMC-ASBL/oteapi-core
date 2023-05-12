"""Pydantic Function Configuration Data Model."""
from pydantic import Field

from oteapi.models.genericconfig import GenericConfig
from oteapi.models.secretconfig import SecretConfig


class FunctionConfig(GenericConfig, SecretConfig):
    """Function Strategy Data Configuration."""

    functionType: str = Field(
        ...,
        description=("Type of registered function strategy."),
    )

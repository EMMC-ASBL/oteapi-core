"""Pydantic Function Configuration Data Model."""
from pydantic import Field

from oteapi.models.genericconfig import GenericConfig


class FunctionConfig(GenericConfig):
    """Function Strategy Data Configuration."""

    functionType: str = Field(
        ...,
        description=("Type of registered function strategy."),
    )

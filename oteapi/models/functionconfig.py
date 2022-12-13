"""Pydantic Function Configuration Data Model."""
from typing import Optional

from pydantic import Field, SecretStr

from oteapi.models.genericconfig import GenericConfig


class FunctionConfig(GenericConfig):
    """Function Strategy Data Configuration."""

    functionType: str = Field(
        ...,
        description=("Type of registered function strategy."),
    )

    secret: Optional[SecretStr] = Field(
        None,
        description="Authorization secret given when executing a function.",
    )

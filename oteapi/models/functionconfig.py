"""Pydantic Function Configuration Data Model."""
from typing import Optional

from pydantic import Field

from oteapi.models.secretconfig import SecretConfig


class FunctionConfig(SecretConfig):
    """Function Strategy Data Configuration."""

    functionType: str = Field(
        ...,
        description=("Type of registered function strategy."),
    )

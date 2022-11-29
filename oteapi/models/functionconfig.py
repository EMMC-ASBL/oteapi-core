"""Pydantic Function Configuration Data Model."""
from typing import Optional

from pydantic import Field

from oteapi.models.genericconfig import GenericConfig


class FunctionConfig(GenericConfig):
    """Function Strategy Data Configuration."""

    functionType: str = Field(
        ...,
        description=("Type of registered function strategy."),
    )

    secret: Optional[str] = Field(
        None,
        description="Authorization secret given when running a transformation.",
    )

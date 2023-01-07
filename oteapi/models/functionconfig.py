"""Pydantic Function Configuration Data Model."""
from typing import Optional

from pydantic import Field

from oteapi.models.genericconfig import GenericConfig
from oteapi.models.secretconfig import SecretConfig


class FunctionConfig(GenericConfig, SecretConfig):  # type: ignore [misc]
    """Function Strategy Data Configuration."""

    functionType: str = Field(
        ...,
        description=("Type of registered function strategy."),
    )

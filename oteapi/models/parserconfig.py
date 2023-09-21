"""Pydantic Parser Configuration Data Model."""
from oteapi.models.genericconfig import GenericConfig
from oteapi.utils._pydantic import Field


class ParserConfig(GenericConfig):
    """Parser Strategy Data Configuration."""

    parserType: str = Field(..., description="Type of registered parser strategy.")

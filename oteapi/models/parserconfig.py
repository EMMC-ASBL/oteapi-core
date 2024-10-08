"""Pydantic Parser Configuration Data Model."""

from __future__ import annotations

from pydantic import AnyHttpUrl, Field

from oteapi.models.genericconfig import GenericConfig


class ParserConfig(GenericConfig):
    """Parser Strategy Data Configuration."""

    parserType: str = Field(..., description="Type of registered parser strategy.")
    entity: AnyHttpUrl = Field(..., description="IRI to the entity or collection.")

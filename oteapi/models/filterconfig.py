"""Pydantic Filter Configuration Data Model."""

from typing import Optional

from pydantic import Field

from oteapi.models.genericconfig import GenericConfig


class FilterConfig(GenericConfig):
    """Filter Strategy Data Configuration."""

    filterType: str = Field(
        ...,
        description="Type of registered filter strategy. E.g., `filter/sql`.",
        json_schema_extra={"IRI": "http://purl.org/dc/terms/type"},
    )
    query: Optional[str] = Field(
        None,
        description="Define a query operation.",
        json_schema_extra={"IRI": "http://www.w3.org/1999/02/22-rdf-syntax-ns#Statement"},
    )
    condition: Optional[str] = Field(
        None,
        description="Logical statement indicating when a filter should be applied.",
        IRI="http://www.w3.org/2000/01/rdf-schema#comment",  # type: ignore
    )
    limit: Optional[int] = Field(
        None,
        description="Number of items remaining after a filter expression.",
        IRI="http://schema.org/Integer",  # type: ignore
    )

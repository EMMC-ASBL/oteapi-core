"""Pydantic Filter Configuration Data Model."""

from __future__ import annotations

from pydantic import Field

from oteapi.models.genericconfig import GenericConfig


class FilterConfig(GenericConfig):
    """Filter Strategy Data Configuration."""

    filterType: str = Field(
        ..., description="Type of registered filter strategy. E.g., `filter/sql`."
    )
    query: str | None = Field(None, description="Define a query operation.")
    condition: str | None = Field(
        None,
        description="Logical statement indicating when a filter should be applied.",
    )
    limit: int | None = Field(
        None, description="Number of items remaining after a filter expression."
    )

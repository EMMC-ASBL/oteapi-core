"""Pydantic Filter Configuration Data Model."""
from typing import Optional

from pydantic import Field

from oteapi.models.genericconfig import GenericConfig


class FilterConfig(GenericConfig):
    """Filter Strategy Data Configuration."""

    filterType: str = Field(
        ..., description="Type of registered filter strategy. E.g., `filter/sql`."
    )
    query: Optional[str] = Field(None, description="Define a query operation.")
    condition: Optional[str] = Field(
        None,
        description="Logical statement indicating when a filter should be applied.",
    )
    limit: Optional[int] = Field(
        None, description="Number of items remaining after a filter expression."
    )

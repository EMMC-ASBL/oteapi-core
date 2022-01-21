"""Pydantic Filter Configuration Data Model."""
from typing import Dict, Optional

from pydantic import BaseModel, Field


class FilterConfig(BaseModel):
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
    configuration: Optional[Dict] = Field(
        None,
        description="Filter-specific configuration options given as key/value-pairs.",
    )

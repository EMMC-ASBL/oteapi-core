"""
Pydantic Filter Configuration Data Model
"""

from typing import Dict, Optional
from pydantic import BaseModel


class FilterConfig(BaseModel):
    """Resource Specific Data Filter Configuration
    query - define a query operation
    condition - logical statement indicating when a filter should be appliced
    limit - number of items remaining after a filter expression
    """

    filterType: str
    query: Optional[str]
    condition: Optional[str]
    limit: Optional[int]
    configuration: Optional[Dict]

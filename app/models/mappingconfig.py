"""
Pydantic Mapping Data Model
"""

from typing import Dict, List, Optional, Tuple

from pydantic import BaseModel


class MappingConfig(BaseModel):
    """Mapping data model"""

    mappingType: str
    prefixes: Optional[Dict[str, str]]
    triples: Optional[List[Tuple[str, str, str]]]
    configuration: Optional[Dict]

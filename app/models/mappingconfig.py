"""
Pydantic Mapping Data Model
"""

from typing import Dict, List, Optional, Tuple

from pydantic import BaseModel, Field


class MappingConfig(BaseModel):
    """Mapping data model"""

    mappingType: str = Field(
        ..., description="Type of registered mapping strategy. E.g., `mapping/demo`."
    )
    prefixes: Optional[Dict[str, str]] = Field(
        None,
        description=(
            "List of shortnames that expands to an IRI "
            "given as localvalue/IRI-expansion-pairs"
        ),
    )
    triples: Optional[List[Tuple[str, str, str]]] = Field(
        None,
        description="List of semantic triples given as (subject, predicate, object).",
    )
    configuration: Optional[Dict] = Field(
        None,
        description="Mapping-specific configuration options given as key/value-pairs.",
    )

"""Pydantic Mapping Configuration Data Model."""
from typing import Annotated, Dict, List, Optional

from pydantic import Field, conlist

from oteapi.models.genericconfig import GenericConfig

SemanticTriple = Annotated[list, conlist(str, min_items=3, max_items=3)]


class MappingConfig(GenericConfig):
    """Mapping Strategy Data Configuration."""

    mappingType: str = Field(
        ..., description="Type of registered mapping strategy. E.g., `mapping/demo`."
    )
    prefixes: Optional[Dict[str, str]] = Field(
        None,
        description=(
            "List of shortnames that expands to an IRI "
            "given as local value/IRI-expansion-pairs."
        ),
    )
    triples: Optional[List[SemanticTriple]] = Field(
        None,
        description="List of semantic triples given as (subject, predicate, object).",
    )

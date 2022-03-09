"""Pydantic Mapping Configuration Data Model."""
from typing import Dict, List, Optional, Tuple

from pydantic import Field

from oteapi.models.genericconfig import GenericConfig


class MappingConfig(GenericConfig):
    """Mapping Strategy Data Configuration."""

    mappingType: str = Field(
        ...,
        description="Type of registered mapping strategy.",
    )
    prefixes: Optional[Dict[str, str]] = Field(
        {},
        description=(
            "List of shortnames that expands to an IRI "
            "given as local value/IRI-expansion-pairs."
        ),
    )
    triples: Optional[List[Tuple[str, str, str]]] = Field(
        [],
        description=(
            "List of semantic triples given as " "(subject, predicate, object)."
        ),
    )

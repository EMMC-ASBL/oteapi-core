"""Pydantic Mapping Configuration Data Model."""
from typing import Dict, List, Optional, Tuple

from pydantic import Field

from oteapi.models.genericconfig import GenericConfig

RDFTriple = Tuple[str, str, str]


class MappingConfig(GenericConfig):
    """Mapping Strategy Data Configuration."""

    mappingType: str = Field(
        ...,
        description="Type of registered mapping strategy.",
    )
    prefixes: Optional[Dict[str, str]] = Field(
        None,
        description=(
            "List of shortnames that expands to an IRI given as local "
            "value/IRI-expansion-pairs."
        ),
    )
    triples: Optional[List[RDFTriple]] = Field(
        None,
        description="List of RDF triples given as (subject, predicate, object).",
    )

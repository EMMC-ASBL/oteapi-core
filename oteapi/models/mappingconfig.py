"""Pydantic Mapping Configuration Data Model."""
from typing import Dict, Optional, Set, Tuple

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
            "Dictionary of shortnames that expands to an IRI given as local "
            "value/IRI-expansion-pairs."
        ),
    )
    triples: Optional[Set[RDFTriple]] = Field(
        None,
        description="Set of RDF triples given as (subject, predicate, object).",
    )

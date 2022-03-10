"""Pydantic Mapping Configuration Data Model."""
from typing import Dict, List, Tuple

from pydantic import Field

from oteapi.models.genericconfig import GenericConfig

RDFTriple = Tuple[str, str, str]


class MappingConfig(GenericConfig):
    """Mapping Strategy Data Configuration."""

    mappingType: str = Field(
        "mapping",
        description="Type of registered mapping strategy.",
    )
    prefixes: Dict[str, str] = Field(
        {},
        description=(
            "List of shortnames that expands to an IRI "
            "given as local value/IRI-expansion-pairs."
        ),
    )
    triples: List[RDFTriple] = Field(
        [],
        description="List of RDF triples given as (subject, predicate, object).",
    )

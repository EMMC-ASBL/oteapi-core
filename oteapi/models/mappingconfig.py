"""Pydantic Mapping Configuration Data Model."""

from __future__ import annotations

from typing import Optional

from pydantic import Field

from oteapi.models.genericconfig import GenericConfig

RDFTriple = tuple[str, str, str]


class MappingConfig(GenericConfig):
    """Mapping Strategy Data Configuration."""

    mappingType: str = Field(
        ...,
        description="Type of registered mapping strategy.",
    )
    prefixes: Optional[dict[str, str]] = Field(
        None,
        description=(
            "Dictionary of shortnames that expands to an IRI given as local "
            "value/IRI-expansion-pairs."
        ),
    )
    triples: Optional[set[RDFTriple]] = Field(
        None,
        description="Set of RDF triples given as (subject, predicate, object).",
    )

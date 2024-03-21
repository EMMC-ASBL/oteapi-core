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
        IRI="http://purl.org/dc/terms/type",  # type: ignore
    )
    prefixes: Optional[Dict[str, str]] = Field(
        None,
        description=(
            "Dictionary of shortnames that expands to an IRI given as local "
            "value/IRI-expansion-pairs."
        ),
        IRI="http://www.w3.org/2004/02/skos/core#notation",  # type: ignore
    )
    triples: Optional[Set[RDFTriple]] = Field(
        None,
        description="Set of RDF triples given as (subject, predicate, object).",
        IRI="http://www.w3.org/1999/02/22-rdf-syntax-ns#Statement",  # type: ignore
    )

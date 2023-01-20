"""Mapping filter strategy."""
# pylint: disable=unused-argument
from typing import TYPE_CHECKING, Dict, List

from pydantic.dataclasses import Field, dataclass

from oteapi.models import MappingConfig, RDFTriple, SessionUpdate

if TYPE_CHECKING:  # pragma: no cover
    from typing import Any, Optional


class MappingSessionUpdate(SessionUpdate):
    """SessionUpdate model for mappings."""

    prefixes: Dict[str, str] = Field(
        ...,
        description=(
            "Dictionary of shortnames that expands to an IRI "
            "given as local value/IRI-expansion-pairs."
        ),
    )
    triples: List[RDFTriple] = Field(
        ...,
        description="List of semantic triples given as (subject, predicate, object).",
    )


@dataclass
class MappingStrategy:
    """Strategy for a mapping.

    The mapping strategy simply adds more prefixes and triples to the
    `prefixes` and `triples` fields in the session such that they are
    available for other strategies, like function strategies that convert
    between data models.

    Nothing is returned to avoid deleting existing mappings.

    **Registers strategies**:

    - `("mappingType", "triples")`

    """

    mapping_config: MappingConfig

    def initialize(
        self, session: "Optional[Dict[str, Any]]" = None
    ) -> MappingSessionUpdate:
        """Initialize strategy."""
        prefixes = session.get("prefixes", {}) if session else {}
        triples = set(session.get("triples", []) if session else [])

        if self.mapping_config.prefixes:
            prefixes.update(self.mapping_config.prefixes)
        if self.mapping_config.triples:
            triples.update(self.mapping_config.triples)

        return MappingSessionUpdate(prefixes=prefixes, triples=triples)

    def get(self, session: "Optional[Dict[str, Any]]" = None) -> SessionUpdate:
        """Execute strategy and return a dictionary."""
        return SessionUpdate()

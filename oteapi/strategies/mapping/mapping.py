"""Mapping filter strategy."""
# pylint: disable=unused-argument
from typing import TYPE_CHECKING

from pydantic.dataclasses import dataclass

from oteapi.models import MappingConfig, SessionUpdate

if TYPE_CHECKING:  # pragma: no cover
    from typing import Any, Dict, Optional


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

    def initialize(self, session: "Optional[Dict[str, Any]]" = None) -> SessionUpdate:
        """Initialize strategy."""
        prefixes = session.get("prefixes", {}) if session else {}
        triples = session.get("triples", []) if session else []

        if self.mapping_config.prefixes:
            prefixes.update(self.mapping_config.prefixes)
        if self.mapping_config.triples:
            triples.extend(self.mapping_config.triples)

        return SessionUpdate(prefixes=prefixes, triples=triples)

    def get(self, session: "Optional[Dict[str, Any]]" = None) -> SessionUpdate:
        """Execute strategy and return a dictionary."""
        return SessionUpdate()

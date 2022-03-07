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
    `prefixes` and `triples` fields in the session.

    Nothing is returned to avoid deleting existing mappings.

    **Registers strategies**:

    - `("filterType", "mapping")`

    """

    config: MappingConfig

    def initialize(self, session: "Optional[Dict[str, Any]]" = None) -> SessionUpdate:
        """Initialize strategy."""
        if session is None:
            raise ValueError("Missing session.")

        if not "prefixes" in session:
            session["prefixes"] = {}

        if not "triples" in session:
            session["triples"] = []

        session["prefixes"].update(self.config.prefixes)
        session["triples"].extend(self.config.triples)

        return SessionUpdate()

    def get(self, session: "Optional[Dict[str, Any]]" = None) -> SessionUpdate:
        """Execute strategy and return a dictionary."""
        return SessionUpdate()

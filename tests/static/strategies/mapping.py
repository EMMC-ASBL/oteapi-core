"""Mapping test strategy class."""

from typing import TYPE_CHECKING

from pydantic.dataclasses import dataclass

from oteapi.models import MappingConfig

if TYPE_CHECKING:
    from typing import Any, Dict, Optional


@dataclass
class MappingTestStrategy:
    """Test mapping strategy."""

    mapping_config: MappingConfig

    def initialize(
        self, session: "Optional[Dict[str, Any]]" = None
    ) -> "Dict[str, Any]":
        """Initialize."""
        return {}

    def get(self, session: "Optional[Dict[str, Any]]" = None) -> "Dict[str, Any]":
        """Run mapping strategy."""
        return {}

"""Mapping Strategy Interface"""
from dataclasses import dataclass
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from typing import Any, Dict, Optional

    from oteapi.models.mappingconfig import MappingConfig


@dataclass  # type: ignore[misc]
class IMappingStrategy(Protocol):
    """Mapping Interface"""

    mapping_config: "MappingConfig"

    def get(self, session: "Optional[Dict[str, Any]]" = None) -> "Dict[str, Any]":
        """Execute strategy and return a dictionary"""

    def initialize(
        self, session: "Optional[Dict[str, Any]]" = None
    ) -> "Dict[str, Any]":
        """Initialize strategy and return a dictionary"""

"""Parse Strategy Interface"""
from dataclasses import dataclass
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from typing import Any, Dict, Optional

    from oteapi.models.resourceconfig import ResourceConfig


@dataclass  # type: ignore[misc]
class IParseStrategy(Protocol):
    """Parse Interfaces"""

    resource_config: "ResourceConfig"

    def parse(self, session: "Optional[Dict[str, Any]]" = None) -> "Dict[str, Any]":
        """run parser and return a dictionary"""

    def initialize(
        self, session: "Optional[Dict[str, Any]]" = None
    ) -> "Dict[str, Any]":
        """Initialize"""

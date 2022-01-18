"""Resource Strategy Interface"""
from dataclasses import dataclass
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from typing import Any, Dict, Optional

    from oteapi.models.resourceconfig import ResourceConfig


@dataclass  # type: ignore[misc]
class IResourceStrategy(Protocol):
    """Resource Interfaces"""

    resource_config: "ResourceConfig"

    def get(self, session: "Optional[Dict[str, Any]]" = None) -> "Dict[str, Any]":
        """Run get-method and return a dictionary"""

    def initialize(
        self, session: "Optional[Dict[str, Any]]" = None
    ) -> "Dict[str, Any]":
        """Initialize"""

"""Filter Strategy Interface"""
from dataclasses import dataclass
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from typing import Any, Dict, Optional

    from oteapi.models.filterconfig import FilterConfig


@dataclass  # type: ignore[misc]
class IFilterStrategy(Protocol):
    """Filter Interface"""

    filter_config: "FilterConfig"

    def get(self, session: "Optional[Dict[str, Any]]" = None) -> "Dict[str, Any]":
        """Execute strategy and return a dictionary"""

    def initialize(
        self, session: "Optional[Dict[str, Any]]" = None
    ) -> "Dict[str, Any]":
        """Initialize strategy and return a dictionary"""

"""Filter test strategy class."""
# pylint: disable=unused-argument,no-self-use
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from typing import Any, Dict, Optional

    from oteapi.models import FilterConfig


@dataclass
class FilterTestStrategy:
    """Test filter strategy."""

    filter_config: "FilterConfig"

    def initialize(
        self, session: "Optional[Dict[str, Any]]" = None
    ) -> "Dict[str, Any]":
        """Initialize."""
        return {}

    def get(self, session: "Optional[Dict[str, Any]]" = None) -> "Dict[str, Any]":
        """Run filter strategy."""
        return {}

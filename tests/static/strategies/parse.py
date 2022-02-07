"""Parse test strategy class."""
# pylint: disable=unused-argument,no-self-use
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from typing import Any, Dict, Optional

    from oteapi.models import ResourceConfig


@dataclass
class ParseTestStrategy:
    """Test parse strategy."""

    parse_config: "ResourceConfig"

    def initialize(
        self, session: "Optional[Dict[str, Any]]" = None
    ) -> "Dict[str, Any]":
        """Initialize."""
        return {}

    def get(self, session: "Optional[Dict[str, Any]]" = None) -> "Dict[str, Any]":
        """Run parse strategy."""
        return {}

"""Function test strategy class."""
# pylint: disable=unused-argument
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any, Dict, Optional

    from oteapi.models import FunctionConfig


@dataclass
class FunctionTestStrategy:
    """Test function strategy."""

    function_config: "FunctionConfig"

    def initialize(
        self, session: "Optional[Dict[str, Any]]" = None
    ) -> "Dict[str, Any]":
        """Initialize."""
        return {}

    def get(self, session: "Optional[Dict[str, Any]]" = None) -> "Dict[str, Any]":
        """Run function strategy."""
        return {}

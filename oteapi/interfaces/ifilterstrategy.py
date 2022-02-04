"""Filter Strategy Interface"""
from dataclasses import dataclass
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:  # pragma: no cover
    from typing import Any, Dict, Optional

    from oteapi.models.filterconfig import FilterConfig


@dataclass  # type: ignore[misc]
class IFilterStrategy(Protocol):
    """Filter Strategy Interface."""

    filter_config: "FilterConfig"

    def get(self, session: "Optional[Dict[str, Any]]" = None) -> "Dict[str, Any]":
        """Execute the strategy.

        Parameters:
            session: A session-specific dictionary context.

        Returns:
            Dictionary of key/value-pairs to be stored in the sessions-specific
            dictionary context.

        """

    def initialize(
        self, session: "Optional[Dict[str, Any]]" = None
    ) -> "Dict[str, Any]":
        """Initialize data class.

        This method will be called through the `/initialize` endpoint of the OTE-API
        Services.

        Parameters:
            session: A session-specific dictionary context.

        Returns:
            Dictionary of key/value-pairs to be stored in the sessions-specific
            dictionary context.

        """

"""Resource Strategy Interface"""
from dataclasses import dataclass
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:  # pragma: no cover
    from typing import Any, Dict, Optional

    from oteapi.models import ResourceConfig, SessionUpdate


@dataclass  # type: ignore[misc]
class IResourceStrategy(Protocol):
    """Resource Strategy Interface."""

    resource_config: "ResourceConfig"

    def get(self, session: "Optional[Dict[str, Any]]" = None) -> "SessionUpdate":
        """Execute the strategy.

        Parameters:
            session: A session-specific dictionary context.

        Returns:
            An update model of key/value-pairs to be stored in the
            session-specific context from services.

        """

    def initialize(self, session: "Optional[Dict[str, Any]]" = None) -> "SessionUpdate":
        """Initialize data class.

        This method will be called through the `/initialize` endpoint of the OTE-API
        Services.

        Parameters:
            session: A session-specific dictionary context.

        Returns:
            An update model of key/value-pairs to be stored in the
            session-specific context from services.

        """

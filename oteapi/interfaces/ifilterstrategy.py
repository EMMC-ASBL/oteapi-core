"""Filter Strategy Interface"""

from dataclasses import dataclass
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:  # pragma: no cover
    from oteapi.models import AttrDict, FilterConfig


@dataclass  # type: ignore[misc]
class IFilterStrategy(Protocol):
    """Filter Strategy Interface."""

    filter_config: "FilterConfig"

    def get(self) -> "AttrDict":
        """Execute the strategy.

        Returns:
            An update model of key/value-pairs to be stored in the
            session-specific context from services.

        """

    def initialize(self) -> "AttrDict":
        """Initialize data class.

        This method will be called through the `/initialize` endpoint of the OTE-API
        Services.

        Returns:
            An update model of key/value-pairs to be stored in the
            session-specific context from services.

        """

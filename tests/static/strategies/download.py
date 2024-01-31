"""Download test strategy class."""

from typing import TYPE_CHECKING

from pydantic.dataclasses import dataclass

from oteapi.models import ResourceConfig

if TYPE_CHECKING:
    from typing import Any, Dict, Optional


@dataclass
class DownloadTestStrategy:
    """Test download strategy."""

    download_config: ResourceConfig

    def initialize(
        self, session: "Optional[Dict[str, Any]]" = None
    ) -> "Dict[str, Any]":
        """Initialize."""
        return {}

    def get(self, session: "Optional[Dict[str, Any]]" = None) -> "Dict[str, Any]":
        """Run download strategy."""
        return {}

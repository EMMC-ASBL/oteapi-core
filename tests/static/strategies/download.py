"""Download test strategy class."""
# pylint: disable=unused-argument
from typing import TYPE_CHECKING

from oteapi.models import ResourceConfig
from oteapi.utils._pydantic import dataclasses as pydantic_dataclasses

if TYPE_CHECKING:
    from typing import Any, Dict, Optional


@pydantic_dataclasses.dataclass
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

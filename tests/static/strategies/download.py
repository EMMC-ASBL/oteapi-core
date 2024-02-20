"""Download test strategy class."""

from typing import TYPE_CHECKING

from pydantic.dataclasses import dataclass

from oteapi.models import AttrDict, ResourceConfig

if TYPE_CHECKING:
    pass


@dataclass
class DownloadTestStrategy:
    """Test download strategy."""

    download_config: ResourceConfig

    def initialize(self) -> AttrDict:
        """Initialize."""
        return AttrDict()

    def get(self) -> AttrDict:
        """Run download strategy."""
        return AttrDict()

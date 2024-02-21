"""Download test strategy class."""

from pydantic.dataclasses import dataclass

from oteapi.models import AttrDict, ResourceConfig


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

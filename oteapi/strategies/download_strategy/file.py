# pylint: disable=W0613, C0103
"""Download strategy class for file"""

from dataclasses import dataclass
from typing import Any, Dict, Optional

from oteapi.datacache.datacache import DataCache
from oteapi.models.resourceconfig import ResourceConfig
from oteapi.strategy-interfaces.factory import StrategyFactory
from pydantic import BaseModel, Extra, Field


class FileConfig(BaseModel):
    """File Specific Configuration"""

    text: bool = Field(
        False, description="Whether the file should be opened in text mode."
    )
    encoding: str = Field(
        None,
        description="Encoding used when opening the file.  "
        "Default is platform dependent.",
    )


@dataclass
@StrategyFactory.register(
    ("scheme", "file"),
)
class FileStrategy:
    """Strategy for retrieving data via local file."""

    resource_config: ResourceConfig

    def initialize(
        self, session: Optional[Dict[str, Any]] = None  # pylint: disable=W0613
    ) -> Dict:
        """Initialize"""
        return {}

    def get(self, session: Optional[Dict[str, Any]] = None) -> Dict:
        """Read local file."""
        assert self.resource_config.downloadUrl
        assert self.resource_config.downloadUrl.scheme == "file"
        filename = self.resource_config.downloadUrl.host

        cache = DataCache(self.resource_config.configuration)
        if cache.config.accessKey and cache.config.accessKey in cache:
            key = cache.config.accessKey
        else:
            config = FileConfig(
                **self.resource_config.configuration, extra=Extra.ignore
            )
            mode = "rt" if config.text else "rb"
            with open(filename, mode, encoding=config.encoding) as f:
                key = cache.add(f.read())

        return {"key": key}

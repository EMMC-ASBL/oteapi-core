"""Download strategy class for the `file` scheme."""
# pylint: disable=unused-argument
from pathlib import Path
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, Field, FileUrl
from pydantic.dataclasses import dataclass

from oteapi.datacache import DataCache
from oteapi.models import ResourceConfig
from oteapi.models.datacacheconfig import DataCacheConfig

if TYPE_CHECKING:  # pragma: no cover
    from typing import Any, Dict


class FileConfig(BaseModel):
    """File-specific Configuration Data Model."""

    text: bool = Field(
        False,
        description=(
            "Whether the file should be opened in text mode. If `False`, the file will"
            " be opened in bytes mode."
        ),
    )
    encoding: Optional[str] = Field(
        None,
        description=(
            "Encoding used when opening the file. The default is platform dependent."
        ),
    )
    cache_config: Optional[DataCacheConfig] = Field(
        None,
        description="Configuration options for the local data cache.",
    )


class FileResourceConfig(ResourceConfig):
    """File download strategy filter config."""

    downloadUrl: FileUrl = Field(
        ..., description="The file URL, which will be downloaded."
    )
    configuration: FileConfig = Field(
        FileConfig(), description="File download strategy-specific configuration."
    )


@dataclass
class FileStrategy:
    """Strategy for retrieving data from a local file.

    **Registers strategies**:

    - `("scheme", "file")`

    """

    download_config: FileResourceConfig

    def initialize(
        self, session: "Optional[Dict[str, Any]]" = None
    ) -> "Dict[str, Any]":
        """Initialize."""
        return {}

    def get(self, session: "Optional[Dict[str, Any]]" = None) -> "Dict[str, Any]":
        """Read local file."""
        filename = Path(self.download_config.downloadUrl.path).resolve()

        if not filename.exists():
            raise FileNotFoundError(f"File not found at {filename}")

        cache = DataCache(self.download_config.configuration.cache_config)
        if cache.config.accessKey and cache.config.accessKey in cache:
            key = cache.config.accessKey
        else:
            key = cache.add(
                filename.read_text(encoding=self.download_config.configuration.encoding)
                if self.download_config.configuration.text
                else filename.read_bytes()
            )

        return {"key": key}

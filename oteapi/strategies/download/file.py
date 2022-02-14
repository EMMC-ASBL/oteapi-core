"""Download strategy class for the `file` scheme."""
# pylint: disable=unused-argument
from dataclasses import dataclass
from pathlib import Path, PosixPath
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, Field

from oteapi.datacache import DataCache
from oteapi.models import SessionUpdate

if TYPE_CHECKING:  # pragma: no cover
    from typing import Any, Dict

    from oteapi.models import ResourceConfig


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


class SessionUpdateFile(SessionUpdate):
    """Class for returning values from Download File strategy."""

    key: str = Field(..., description="Key to access the data in the cache.")


@dataclass
class FileStrategy:
    """Strategy for retrieving data from a local file.

    **Registers strategies**:

    - `("scheme", "file")`

    """

    download_config: "ResourceConfig"

    def initialize(self, session: "Optional[Dict[str, Any]]" = None) -> SessionUpdate:
        """Initialize."""
        return SessionUpdate()

    def get(self, session: "Optional[Dict[str, Any]]" = None) -> SessionUpdateFile:
        """Read local file."""
        if (
            self.download_config.downloadUrl is None
            or self.download_config.downloadUrl.scheme != "file"
        ):
            raise ValueError(
                "Expected 'downloadUrl' to have scheme 'file' in the configuration."
            )

        filename = Path(self.download_config.downloadUrl.path).resolve()
        if isinstance(filename, PosixPath):
            filename = Path("/" + self.download_config.downloadUrl.host + str(filename))

        cache = DataCache(self.download_config.configuration)
        if cache.config.accessKey and cache.config.accessKey in cache:
            key = cache.config.accessKey
        else:
            config = FileConfig(**self.download_config.configuration)
            key = cache.add(
                filename.read_text(encoding=config.encoding)
                if config.text
                else filename.read_bytes()
            )

        return SessionUpdateFile(key=key)

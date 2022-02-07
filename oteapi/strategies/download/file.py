"""Download strategy class for the `file` scheme."""
# pylint: disable=unused-argument
from dataclasses import dataclass
from pathlib import Path
from platform import system
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, Extra, Field

from oteapi.datacache import DataCache

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


@dataclass
class FileStrategy:
    """Strategy for retrieving data from a local file.

    **Registers strategies**:

    - `("scheme", "file")`

    """

    download_config: "ResourceConfig"

    def initialize(
        self, session: "Optional[Dict[str, Any]]" = None
    ) -> "Dict[str, Any]":
        """Initialize."""
        return {}

    def get(self, session: "Optional[Dict[str, Any]]" = None) -> "Dict[str, Any]":
        """Read local file."""
        if (
            self.download_config.downloadUrl is None
            or self.download_config.downloadUrl.scheme != "file"
        ):
            raise ValueError(
                "Expected 'downloadUrl' to have scheme 'file' in the configuration."
            )

        if system() == "Windows":
            filename = Path(
                self.resource_config.downloadUrl.host
                + ":"
                + self.resource_config.downloadUrl.path
            ).resolve()
        else:
            host = self.resource_config.downloadUrl.host
            path = str(Path(self.resource_config.downloadUrl.path).resolve())
            filename = Path("/" + host + path)

        cache = DataCache(self.download_config.configuration)
        if cache.config.accessKey and cache.config.accessKey in cache:
            key = cache.config.accessKey
        else:
            config = FileConfig(
                **self.resource_config.configuration.dict(), extra=Extra.ignore
            )
            key = cache.add(
                filename.read_text(encoding=config.encoding)
                if config.text
                else filename.read_bytes()
            )

        return {"key": key}

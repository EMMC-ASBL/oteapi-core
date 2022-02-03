"""Download strategy class for the `file` scheme."""
# pylint: disable=unused-argument
from dataclasses import dataclass
from pathlib import Path
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

        filename = Path(self.download_config.downloadUrl.host).resolve()

        cache = DataCache(self.download_config.configuration)
        if cache.config.accessKey and cache.config.accessKey in cache:
            key = cache.config.accessKey
        else:
            config = FileConfig(
                **self.download_config.configuration, extra=Extra.ignore
            )
            key = cache.add(
                filename.read_text(encoding=config.encoding)
                if config.text
                else filename.read_bytes()
            )

        return {"key": key}

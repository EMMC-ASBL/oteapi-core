"""Download strategy class for the `file` scheme."""
# pylint: disable=unused-argument
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Optional
from urllib.parse import urlparse

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

        filename = Path(urlparse(self.download_config.downloadUrl).path)

        # Grr, urlparse() leaving an initial slash in front of the drive
        # letter when parsing a file url for an absolute path on Windows.
        # Example: urlparse("file:///C:/Windows") -> "/C:/Windows"
        #
        # Workaround: remove the initial slash in these cases.

        print(
            "*****************************************************************",
            file=sys.stderr,
        )
        print(f"*** filename: {filename}", file=sys.stderr)
        print(f"*** platform: {sys.platform}", file=sys.stderr)

        if sys.platform.startswith("win"):
            print("  * on Windows", file=sys.stderr)
            if re.match(r"^\\[a-zA-Z]:\\", str(filename)):
                print("  * match", file=sys.stderr)
                filename = Path(str(filename)[1:])

        print(f"--> filename: {filename}", file=sys.stderr)
        print(
            "*****************************************************************",
            file=sys.stderr,
        )

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

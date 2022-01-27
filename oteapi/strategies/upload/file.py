"""Upload strategy class for the `file` scheme."""
# pylint: disable=unused-argument
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, Field

from oteapi.datacache import DataCache
from oteapi.plugins import StrategyFactory

if TYPE_CHECKING:
    from typing import Any, Dict

    from oteapi.models import ResourceConfig


class FileConfig(BaseModel):
    """File-specific Configuration Data Model."""

    accessKey: str = Field(
        None,
        description="Datacache key with which the content to upload can be accessed.",
    )
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
@StrategyFactory.register(("uploadScheme", "file"))
class FileUploadStrategy:
    """Strategy for writing data from a local file.

    **Registers strategies**:

    - `("scheme", "file")`

    """

    resource_config: "ResourceConfig"

    def initialize(
        self, session: "Optional[Dict[str, Any]]" = None
    ) -> "Dict[str, Any]":
        """Initialize."""
        return {}

    def get(self, session: "Optional[Dict[str, Any]]" = None):
        """Write local file.

        The file content is obtained with the `accessKey` DataCache
        configuration and the filename from the `accessUrl`
        ResourceConfig configuration.
        """
        if (
            self.resource_config.accessUrl is None
            or self.resource_config.accessUrl.scheme != "file"
        ):
            raise ValueError(
                "Expected 'accessUrl' to have scheme 'file' in the configuration."
            )

        config = FileConfig(**self.resource_config.configuration)
        cache = DataCache()
        if not config.accessKey or config.accessKey not in cache:
            raise ValueError("Expected  a valid 'accessKey' in the configurations.")

        raw = cache.get(cache.config.accessKey)
        if config.encoding:
            content = str(raw, encoding=config.encoding)
        else:
            content = str(raw)

        filename = Path(self.resource_config.accessUrl.host).resolve()
        mode = "wt" if config.text else "w"
        with open(filename, mode, encoding="UTF-8") as handle:
            handle.write(content)

"""Strategy class for sftp/ftp"""
# pylint: disable=unused-argument
from dataclasses import dataclass
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import TYPE_CHECKING, Optional
from pydantic import Field

import pysftp

from oteapi.datacache import DataCache

from oteapi.models.sessionupdate import SessionUpdate

if TYPE_CHECKING:  # pragma: no cover
    from typing import Any, Dict, Optional

    from oteapi.models import ResourceConfig

class SessionUpdateSFTP(SessionUpdate):
    """Class for returning values from Download SFTP strategy."""

    key: Optional[str] = Field(
        None,
        description="Key to access the data in the cache.",
    )

@dataclass
class SFTPStrategy:
    """Strategy for retrieving data via sftp.

    **Registers strategies**:

    - `("scheme", "ftp")`
    - `("scheme", "sftp")`

    """

    download_config: "ResourceConfig"

    def initialize(
        self, session: "Optional[Dict[str, Any]]" = None
    ) -> SessionUpdate:
        """Initialize."""
        return {}

    def get(self, session: "Optional[Dict[str, Any]]" = None) -> SessionUpdateSFTP:
        """Download via sftp"""
        cache = DataCache(self.download_config.configuration)
        if cache.config.accessKey and cache.config.accessKey in cache:
            key = cache.config.accessKey
        else:
            # Setup connection options
            cnopts = pysftp.CnOpts()
            cnopts.hostkeys = None

            if not self.download_config.downloadUrl:
                raise ValueError("downloadUrl is not defined in configuration.")

            # open connection and store data locally
            with pysftp.Connection(
                host=self.download_config.downloadUrl.host,
                username=self.download_config.downloadUrl.user,
                password=self.download_config.downloadUrl.password,
                port=self.download_config.downloadUrl.port,
                cnopts=cnopts,
            ) as sftp:
                # Because of insane locking on Windows, we have to close
                # the downloaded file before adding it to the cache
                with NamedTemporaryFile(prefix="oteapi-sftp-", delete=False) as handle:
                    localpath = Path(handle.name).resolve()
                try:
                    sftp.get(self.download_config.downloadUrl.path, localpath=localpath)
                    key = cache.add(localpath.read_bytes())
                finally:
                    localpath.unlink()

        return SessionUpdateSFTP(key=key)

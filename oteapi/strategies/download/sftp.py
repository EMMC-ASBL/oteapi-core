"""Strategy class for sftp/ftp"""
from dataclasses import dataclass
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import TYPE_CHECKING

import pysftp

from oteapi.datacache import DataCache
from oteapi.plugins import StrategyFactory

if TYPE_CHECKING:
    from typing import Any, Dict

    from oteapi.models import ResourceConfig


@dataclass
@StrategyFactory.register(("scheme", "sftp"), ("scheme", "ftp"))
class SFTPStrategy:
    """Strategy for retrieving data via sftp.

    **Registers strategies**:

    - `("scheme", "ftp")`
    - `("scheme", "sftp")`

    """

    resource_config: "ResourceConfig"

    def initialize(self, **_) -> "Dict[str, Any]":
        """Initialize."""
        return {}

    def get(self, **_) -> "Dict[str, Any]":
        """Download via sftp"""
        cache = DataCache(self.resource_config.configuration)
        if cache.config.accessKey and cache.config.accessKey in cache:
            key = cache.config.accessKey
        else:
            # Setup connection options
            cnopts = pysftp.CnOpts()
            cnopts.hostkeys = None

            if not self.resource_config.accessUrl:
                raise ValueError("accessUrl is not defined in configuration.")

            # open connection and store data locally
            with pysftp.Connection(
                host=self.resource_config.accessUrl.host,
                username=self.resource_config.accessUrl.user,
                password=self.resource_config.accessUrl.password,
                port=self.resource_config.accessUrl.port,
                cnopts=cnopts,
            ) as sftp:
                # Because of insane locking on Windows, we have to close
                # the downloaded file before adding it to the cache
                with NamedTemporaryFile(prefix="oteapi-sftp-", delete=False) as handle:
                    localpath = Path(handle.name).resolve()
                try:
                    sftp.get(self.resource_config.accessUrl.path, localpath=localpath)
                    key = cache.add(localpath.read_bytes())
                finally:
                    localpath.unlink()

        return {"key": key}

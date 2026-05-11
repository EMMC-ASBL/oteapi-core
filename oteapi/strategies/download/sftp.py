"""Strategy class for sftp/ftp"""

from __future__ import annotations

from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Annotated

import paramiko
from pydantic import Field
from pydantic.dataclasses import dataclass
from pydantic.networks import AnyUrl, UrlConstraints

from oteapi.datacache import DataCache
from oteapi.models import AttrDict, DataCacheConfig, ResourceConfig

AnyFtpUrl = Annotated[AnyUrl, UrlConstraints(allowed_schemes=["ftp", "sftp"])]


class SFTPConfig(AttrDict):
    """(S)FTP-specific Configuration Data Model."""

    datacache_config: DataCacheConfig | None = Field(
        None,
        description=(
            "Configurations for the data cache for storing the downloaded file "
            "content."
        ),
    )


class SFTPResourceConfig(ResourceConfig):
    """(S)FTP download strategy filter config."""

    downloadUrl: AnyFtpUrl = Field(  # type: ignore[assignment]
        ..., description="The (S)FTP URL, which will be downloaded."
    )
    configuration: SFTPConfig = Field(
        SFTPConfig(), description="(S)FTP download strategy-specific configuration."
    )


class SFTPContent(AttrDict):
    """Class for returning values from Download SFTP strategy."""

    key: str = Field(..., description="Key to access the data in the cache.")


@dataclass
class SFTPStrategy:
    """Strategy for retrieving data via sftp.

    **Registers strategies**:

    - `("scheme", "ftp")`
    - `("scheme", "sftp")`

    """

    download_config: SFTPResourceConfig

    def initialize(self) -> AttrDict:
        """Initialize."""
        return AttrDict()

    def get(self) -> SFTPContent:
        """Download via sftp"""
        url = self.download_config.downloadUrl
        if not url.host or not url.path:
            raise ValueError(
                "Invalid (S)FTP URL (missing host or path): "
                f"host={url.host!r}, path={url.path!r}"
            )

        cache = DataCache(self.download_config.configuration.datacache_config)
        if cache.config.accessKey and cache.config.accessKey in cache:
            key = cache.config.accessKey
        else:
            with paramiko.SSHClient() as client:
                client.set_missing_host_key_policy(
                    paramiko.AutoAddPolicy()
                )  # nosec B507
                client.connect(
                    hostname=url.host,
                    username=url.username,
                    password=url.password,
                    port=url.port or 22,
                )
                # Because of insane locking on Windows, we have to close
                # the downloaded file before adding it to the cache
                with NamedTemporaryFile(prefix="oteapi-sftp-", delete=False) as handle:
                    localpath = Path(handle.name).resolve()
                try:
                    with client.open_sftp() as sftp:
                        sftp.get(url.path, str(localpath))
                    key = cache.add(localpath.read_bytes())
                finally:
                    localpath.unlink()

        return SFTPContent(key=key)

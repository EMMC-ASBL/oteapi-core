""" Strategy class for image/jpg """

from dataclasses import dataclass
from typing import Any, Dict, Optional

import pysftp

from app.models.resourceconfig import ResourceConfig
from app.strategy.factory import StrategyFactory


@dataclass
@StrategyFactory.register(("scheme", "sftp"), ("scheme", "ftp"))
class SFTPStrategy:
    """strategy for retrieving data via sftp"""

    resource_config: ResourceConfig

    def initialize(
        self, session: Optional[Dict[str, Any]] = None  # pylint: disable=W0613
    ) -> Dict:
        """Initialize"""
        return dict()

    def read(
        self, session: Optional[Dict[str, Any]] = None  # pylint: disable=W0613
    ) -> Dict:
        """Download via sftp"""

        # Setup connection options
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None

        # open connection and store data locally
        with pysftp.Connection(
            host=self.resource_config.accessUrl.host,
            username=self.resource_config.accessUrl.user,
            password=self.resource_config.accessUrl.password,
            port=self.resource_config.accessUrl.port,
            cnopts=cnopts,
        ) as sftp:
            # Here we just extract the filename and store the downloaded
            # file to /ote-data/<filename>
            filename = self.resource_config.accessUrl.path.split("/")[-1]
            localpath = f"/ote-data/{filename}"
            sftp.get(self.resource_config.accessUrl.path, localpath=localpath)
            return dict(filename=localpath)

        return dict()

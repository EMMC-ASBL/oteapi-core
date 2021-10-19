""" Strategy class for image/jpg """

from dataclasses import dataclass
from typing import Dict, Optional, Any
import pysftp
from app.strategy import factory
from app.models.resourceconfig import ResourceConfig


@dataclass
class SFTPStrategy:
    """ strategy for retrieving data via sftp """

    resource_config: ResourceConfig

    def read(self, session: Optional[Dict[str, Any]] = None) -> Dict: #pylint: disable=W0613
        """ Download via sftp """

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
            # file to ./data/<filename>
            filename = self.resource_config.accessUrl.path.split('/')[-1]
            localpath=f'./data/{filename}'
            sftp.get(self.resource_config.accessUrl.path, localpath=localpath)
            return dict(filename=localpath)

        return dict()


def initialize() -> None:
    """ register download strategy """
    factory.register_download_strategy("sftp", SFTPStrategy)
    factory.register_download_strategy("ftp", SFTPStrategy)

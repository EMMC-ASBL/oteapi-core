""" Strategy class for image/jpg """

from dataclasses import dataclass
from app.strategy import factory
from typing import Dict
from app.models.resourceconfig import ResourceConfig
import pysftp
import os

@dataclass
class SFTPStrategy:
    """ strategy for retrieving data via sftp """

    resource_config: ResourceConfig

    def read(self) -> Dict:
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
            localpath=f'./data/{self._filename}'
            sftp.get(self.resource_config.accessUrl.path, localpath=localpath)
            return dict(filename=localpath)

        return dict()


def initialize() -> None:
    """ register download strategy """
    factory.register_download_strategy("sftp", SFTPStrategy)
    factory.register_download_strategy("ftp", SFTPStrategy)
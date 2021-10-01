""" Strategy class for image/jpg """

from dataclasses import dataclass
from app import factory
from typing import Dict
import pysftp
import os

@dataclass
class SFTPStrategy:
    """ strategy for retrieving data via sftp """

    def __init__(self, **kwargs):
        self._configuration = kwargs.get('configuration')
        self._uri = kwargs.get('url')
        self._username= kwargs.get('username')
        self._password= kwargs.get('password')
        self._port = int(kwargs.get('port', '22'))
        self._hostname = kwargs.get('hostname')
        self._path = kwargs.get('path')
        self._filename = os.path.basename(self._path)

    def read(self) -> Dict:
        """ Download via sftp """

        # Setup connection options
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None

        # open connection and store data locally
        with pysftp.Connection(
            host=self._hostname,
            username=self._username,
            password=self._password,
            port=self._port,
            cnopts=cnopts,
        ) as sftp:
            localpath=f'./data/{self._filename}'
            sftp.get(self._path, localpath=localpath)
            return dict(filename=localpath)

        return dict()


def initialize() -> None:
    """ register download strategy """
    factory.register_download_strategy("sftp", SFTPStrategy)
    factory.register_download_strategy("ftp", SFTPStrategy)
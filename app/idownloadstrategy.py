"""
Download Strategy Interface
"""
from typing import Protocol, Dict

class IDownloadStrategy(Protocol): # pylint: disable=R0903
    """ Data Storage Interfaces"""

    def read(self) -> Dict:
        """ Pretend to do something """

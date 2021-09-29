"""
Data Storage Interface
"""
from typing import Protocol, Dict

class IParseStrategy(Protocol): # pylint: disable=R0903
    """ Data Storage Interfaces"""

    def parse(self) -> Dict:
        """ run parser and return a dictionary """

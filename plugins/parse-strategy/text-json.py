""" Strategy class for text/json """

from app import factory
from typing import Dict


class JSONDataParseStrategy:

    def __init__(self, **kwargs):
        self._configuration = kwargs.get('configuration')

    def parse(self) -> Dict:
        print ("JSON in action!")
        return dict(status='ok')

def initialize() -> None:
    factory.register_parse_strategy("text/json", JSONDataParseStrategy)

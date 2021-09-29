""" Strategy class for text/csv """

from app import factory
from typing import Dict


class CSVParseStrategy:

    def parse(self) -> Dict:
        print ("CSV in action!")
        return dict(status="ok")


def initialize() -> None:
    factory.register_parse_strategy("text/csv", CSVParseStrategy)


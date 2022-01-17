"""`oteapi.interfaces` module.

This module hosts the strategy interfaces.
The strategy interfaces can be considered to be the abstract classes for the
strategies.
"""
from .idownloadstrategy import IDownloadStrategy
from .ifilterstrategy import IFilterStrategy
from .imappingstrategy import IMappingStrategy
from .iparsestrategy import IParseStrategy
from .iresourcestrategy import IResourceStrategy
from .itransformationstrategy import ITransformationStrategy


__all__ = (
    "IDownloadStrategy",
    "IFilterStrategy",
    "IMappingStrategy",
    "IParseStrategy",
    "IResourceStrategy",
    "ITransformationStrategy",
)

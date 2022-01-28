"""`oteapi.interfaces` module.

This module hosts the strategy interfaces.
The strategy interfaces can be considered to be the abstract classes for the
strategies.
"""
from typing import Union

from .idownloadstrategy import IDownloadStrategy
from .ifilterstrategy import IFilterStrategy
from .imappingstrategy import IMappingStrategy
from .iparsestrategy import IParseStrategy
from .iresourcestrategy import IResourceStrategy
from .iserialisestrategy import ISerialiseStrategy
from .itransformationstrategy import ITransformationStrategy
from .iuploadstrategy import IUploadStrategy

__all__ = (
    "IDownloadStrategy",
    "IFilterStrategy",
    "IMappingStrategy",
    "IParseStrategy",
    "IResourceStrategy",
    "ISerialiseStrategy",
    "IStrategy",
    "ITransformationStrategy",
    "IUploadStrategy",
)

IStrategy = Union[
    IDownloadStrategy,
    IFilterStrategy,
    IMappingStrategy,
    IParseStrategy,
    IResourceStrategy,
    ISerialiseStrategy,
    ITransformationStrategy,
    IUploadStrategy,
]

"""`oteapi.models` module.

This module contains all the `pydantic` configuration models.
"""

from __future__ import annotations

from typing import Union

from .datacacheconfig import DataCacheConfig
from .filterconfig import FilterConfig
from .functionconfig import FunctionConfig
from .genericconfig import AttrDict, GenericConfig
from .mappingconfig import MappingConfig, RDFTriple
from .parserconfig import ParserConfig
from .resourceconfig import HostlessAnyUrl, ResourceConfig
from .secretconfig import SecretConfig
from .transformationconfig import TransformationConfig, TransformationStatus
from .triplestoreconfig import TripleStoreConfig

__all__ = (
    "AttrDict",
    "AttrDict",
    "DataCacheConfig",
    "FilterConfig",
    "FunctionConfig",
    "GenericConfig",
    "HostlessAnyUrl",
    "MappingConfig",
    "ParserConfig",
    "RDFTriple",
    "ResourceConfig",
    "SecretConfig",
    "StrategyConfig",
    "TransformationConfig",
    "TransformationStatus",
    "TripleStoreConfig",
)

StrategyConfig = Union[
    FilterConfig,
    FunctionConfig,
    MappingConfig,
    ParserConfig,
    ResourceConfig,
    TransformationConfig,
]

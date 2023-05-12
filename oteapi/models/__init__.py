"""`oteapi.models` module.

This module contains all the `pydantic` configuration models.
"""
from typing import Union

from .datacacheconfig import DataCacheConfig
from .filterconfig import FilterConfig
from .functionconfig import FunctionConfig
from .genericconfig import AttrDict, GenericConfig
from .mappingconfig import MappingConfig, RDFTriple
from .resourceconfig import ResourceConfig
from .secretconfig import SecretConfig
from .sessionupdate import SessionUpdate
from .transformationconfig import TransformationConfig, TransformationStatus
from .triplestoreconfig import TripleStoreConfig

__all__ = (
    "AttrDict",
    "DataCacheConfig",
    "FilterConfig",
    "FunctionConfig",
    "GenericConfig",
    "MappingConfig",
    "RDFTriple",
    "ResourceConfig",
    "SessionUpdate",
    "StrategyConfig",
    "TransformationConfig",
    "TransformationStatus",
    "TripleStoreConfig",
    "SecretConfig",
)

StrategyConfig = Union[
    FilterConfig, FunctionConfig, MappingConfig, ResourceConfig, TransformationConfig
]

"""`oteapi.models` module.

This module contains all the `pydantic` configuration models.
"""
from typing import Union

from .datacacheconfig import DataCacheConfig
from .filterconfig import FilterConfig
from .functionconfig import FunctionConfig
from .genericconfig import AttrDict, GenericConfig
from .mappingconfig import MappingConfig
from .resourceconfig import ResourceConfig
from .transformationconfig import TransformationConfig, TransformationStatus
from .sessionupdate import SessionUpdate

__all__ = (
    "AttrDict",
    "DataCacheConfig",
    "FilterConfig",
    "FunctionConfig",
    "GenericConfig",
    "MappingConfig",
    "ResourceConfig",
    "StrategyConfig",
    "TransformationConfig",
    "TransformationStatus",
    "SessionUpdate",
)

StrategyConfig = Union[
    FilterConfig, FunctionConfig, MappingConfig, ResourceConfig, TransformationConfig
]

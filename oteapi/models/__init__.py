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
from .sessionupdate import SessionUpdate
from .transformationconfig import TransformationConfig, TransformationStatus

__all__ = (
    "AttrDict",
    "DataCacheConfig",
    "FilterConfig",
    "FunctionConfig",
    "GenericConfig",
    "MappingConfig",
    "ResourceConfig",
    "SessionUpdate",
    "StrategyConfig",
    "TransformationConfig",
    "TransformationStatus",
)

StrategyConfig = Union[
    FilterConfig, FunctionConfig, MappingConfig, ResourceConfig, TransformationConfig
]

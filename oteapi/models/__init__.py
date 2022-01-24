"""`oteapi.models` module.

This module contains all the `pydantic` configuration models.
"""
from typing import Union

from .datacacheconfig import DataCacheConfig
from .filterconfig import FilterConfig
from .mappingconfig import MappingConfig
from .resourceconfig import ResourceConfig
from .transformationconfig import TransformationConfig, TransformationStatus

__all__ = (
    "DataCacheConfig",
    "FilterConfig",
    "MappingConfig",
    "ResourceConfig",
    "StrategyConfig",
    "TransformationConfig",
    "TransformationStatus",
)

StrategyConfig = Union[
    FilterConfig, MappingConfig, ResourceConfig, TransformationConfig
]

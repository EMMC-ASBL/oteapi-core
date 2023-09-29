"""Pydantic Transformation Configuration Data Model.

A transformation status data model is provided as well.
This data model represents what should be returned from the strategy's `status()`
method.
"""
from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field

from oteapi.models.genericconfig import GenericConfig
from oteapi.models.secretconfig import SecretConfig


class ProcessPriority(str, Enum):
    """Defining process priority enumerators.

    Process priorities:

    - Low
    - Medium
    - High

    """

    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


class TransformationConfig(GenericConfig, SecretConfig):
    """Transformation Strategy Data Configuration."""

    transformationType: str = Field(
        ...,
        description=(
            "Type of registered transformation strategy. E.g., `celery/remote`."
        ),
    )
    name: Optional[str] = Field(
        None, description="Human-readable name of the transformation strategy."
    )
    due: Optional[datetime] = Field(
        None,
        description=(
            "Optional field to indicate a due data/time for when a transformation "
            "should finish."
        ),
    )
    priority: Optional[ProcessPriority] = Field(
        ProcessPriority.MEDIUM,
        description="Define the process priority of the transformation execution.",
    )


class TransformationStatus(BaseModel):
    """Return from transformation status."""

    id: str = Field(..., description="ID for the given transformation process.")
    status: Optional[str] = Field(
        None, description="Status for the transformation process."
    )
    messages: Optional[List[str]] = Field(
        None, description="Messages related to the transformation process."
    )
    created: Optional[datetime] = Field(
        None,
        description="Time of creation for the transformation process. Given in UTC.",
    )
    startTime: Optional[datetime] = Field(
        None, description="Time when the transformation process started. Given in UTC."
    )
    finishTime: Optional[datetime] = Field(
        None, description="Time when the tranformation process finished. Given in UTC."
    )

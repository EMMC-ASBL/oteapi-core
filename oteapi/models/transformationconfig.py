"""Pydantic Transformation Configuration Data Model.

A transformation status data model is provided as well.
This data model represents what should be returned from the strategy's `status()`
method.
"""
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class PriorityEnum(str, Enum):
    """Defining process priority enumerators.

    Process priorities:

    - Low
    - Medium
    - High

    """

    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


class TransformationConfig(BaseModel):
    """Transformation Strategy Data Configuration.

    Attributes:
        transformation_type: Type of registered transformation strategy. E.g.,
            `celery/remote`.
        name: Human-readable name of the transformation strategy.
        description: A free-text account of the transformation.
        due: Optional field to indicate a due data/time for when a transformation
            should finish.
        priority: Define the process priority of the transformation execution.
        secret: Authorization secret given when running a transformation.
        configuration: Transformation-specific configuration options given as
            key/value-pairs.

    """

    transformation_type: str = Field(
        ...,
        description=(
            "Type of registered transformation strategy. E.g., `celery/remote`."
        ),
    )
    name: Optional[str] = Field(
        None, description="Human-readable name of the transformation strategy."
    )
    description: Optional[str] = Field(
        None, description="A free-text account of the transformation."
    )
    due: Optional[datetime] = Field(
        None,
        description=(
            "Optional field to indicate a due data/time for when a transformation "
            "should finish."
        ),
    )
    priority: Optional[PriorityEnum] = Field(
        PriorityEnum.MEDIUM,
        description="Define the process priority of the transformation execution.",
    )
    secret: Optional[str] = Field(
        None,
        description="Authorization secret given when running a transformation.",
    )
    configuration: Optional[Dict] = Field(
        None,
        description=(
            "Transformation-specific configuration options given as key/value-pairs."
        ),
    )


class TransformationStatus(BaseModel):
    """Return from transformation status.

    Attributes:
        id: ID for the given transformation process.
        status: Status for the transformation process.
        messages: Messages related to the transformation process.
        created: Time of creation for the transformation process. Given in UTC.
        startTime: Time when the transformation process started. Given in UTC.
        finishTime: Time when the tranformation process finished. Given in UTC.

    """

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

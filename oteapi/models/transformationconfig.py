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
        IRI="http://purl.org/dc/terms/type",  # type: ignore
    )
    name: Optional[str] = Field(
        None,
        description="Human-readable name of the transformation strategy.",
        IRI="http://purl.org/dc/terms/title",  # type: ignore
    )
    due: Optional[datetime] = Field(
        None,
        description=(
            "Optional field to indicate a due data/time for when a transformation "
            "should finish."
        ),
        IRI="http://purl.org/dc/terms/date",  # type: ignore
    )
    priority: Optional[ProcessPriority] = Field(
        ProcessPriority.MEDIUM,
        description="Define the process priority of the transformation execution.",
        IRI="http://www.w3.org/ns/adms#status",  # type: ignore
    )


class TransformationStatus(BaseModel):
    """Return from transformation status."""

    id: str = Field(
        ...,
        description="ID for the given transformation process.",
        IRI="http://purl.org/dc/terms/identifier",  # type: ignore
    )
    status: Optional[str] = Field(
        None,
        description="Status for the transformation process.",
        IRI="http://www.w3.org/ns/adms#status",  # type: ignore
    )
    messages: Optional[List[str]] = Field(
        None,
        description="Messages related to the transformation process.",
        IRI="http://purl.org/dc/terms/description",  # type: ignore
    )
    created: Optional[datetime] = Field(
        None,
        description="Time of creation for the transformation process. Given in UTC.",
        IRI="http://purl.org/dc/terms/created",  # type: ignore
    )
    startTime: Optional[datetime] = Field(
        None,
        description="Time when the transformation process started. Given in UTC.",
        IRI="http://purl.org/dc/terms/date",  # type: ignore
    )
    finishTime: Optional[datetime] = Field(
        None,
        description="Time when the tranformation process finished. Given in UTC.",
        IRI="http://purl.org/dc/terms/date",  # type: ignore
    )

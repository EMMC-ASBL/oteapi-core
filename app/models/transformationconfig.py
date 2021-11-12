"""
TransformationConfig data model definition
"""

from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class TransformationConfig(BaseModel):
    """Transformation data model"""

    transformation_type: str = Field(
        ...,
        description="Type of registered transformation strategy. E.g., `dlite/transformation`.",
    )
    name: Optional[str] = Field(
        None, description="Human-readable name of the transformation strategy."
    )
    description: Optional[str] = Field(
        None, description="A free-text account of the transformation."
    )
    due: Optional[datetime] = Field(None, description="")
    priority: Optional[int] = Field(None, description="")
    secret: Optional[str] = Field(None, description="")
    configuration: Optional[Dict] = Field(
        None,
        description="Transformation-specific configuration options given as key/value-pairs.",
    )


class TransformationStatus(BaseModel):
    """Return from transformation status"""

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

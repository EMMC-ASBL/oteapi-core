"""
TransformationConfig data model definition
"""

from typing import Dict, Optional, List
from datetime import datetime
from pydantic import BaseModel


class TransformationConfig(BaseModel):
    """Transformation data model"""

    transformation_type: str
    name: Optional[str]
    description: Optional[str]
    due: Optional[datetime]
    priority: Optional[int]
    secret: Optional[str]
    configuration: Optional[Dict]


class TransformationStatus(BaseModel):
    """Return from transformation status"""

    id: str
    status: Optional[str]
    messages: Optional[List[str]]
    created: Optional[datetime]
    startTime: Optional[datetime]
    finishTime: Optional[datetime]

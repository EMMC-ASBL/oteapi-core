"""
TransformationConfig data model definition
"""

from datetime import datetime
from typing import Dict, List, Optional

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
    status: str
    messages: List[str]
    created: datetime
    startTime: datetime
    finishTime: datetime

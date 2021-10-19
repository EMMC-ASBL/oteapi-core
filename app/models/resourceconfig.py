"""
Pydantic ResourceConfig Data Model
"""

from typing import Dict, Optional
from pydantic import BaseModel, AnyUrl

class ResourceConfig(BaseModel):
    """ Dataset distributrion """
    downloadUrl: AnyUrl
    mediaType: str
    accessUrl: Optional[AnyUrl] # doc
    license: Optional[str]
    accessRights: Optional [str]
    description: Optional [str]
    published: Optional [str]
    configuration: Optional[Dict] = None

"""
Data Source context
"""
from uuid import uuid4
import json

from typing import Dict, Any, Optional
from fastapi import APIRouter, Depends
from fastapi_plugins import depends_redis
from aioredis import Redis
from pydantic import BaseModel
from app import factory
from .session import _update_session, _update_session_list_item
import dlite


router = APIRouter()

IDPREDIX = 'filter-'

class FilterConfig(BaseModel):
    filter_type: str
    configuration: Optional[Dict]


@router.post('/')
async def create_filter(
    config: FilterConfig,
    session_id: Optional[str] = None,
    cache: Redis = Depends(depends_redis),
) -> Dict:
    """ Define a new filter configuration (data operation) """
    return dict(status='ok')


@router.get('/{filter_id}')
async def get_filter(
    filter_id: str,
    session_id: Optional[str] = None,
    cache: Redis = Depends(depends_redis),
) -> Dict:
    """ Run and return data from a   filter (data operation) """
    return dict(status='ok')

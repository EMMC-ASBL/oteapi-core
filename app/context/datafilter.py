"""
Data Source context
"""
from uuid import uuid4
import json

from typing import Dict, Optional
from fastapi import APIRouter, Depends
from fastapi_plugins import depends_redis
from aioredis import Redis
from app.strategy import factory
from app.models.filterconfig import FilterConfig
from .session import _update_session, _update_session_list_item


router = APIRouter()

IDPREDIX = 'filter-'

@router.post('/')
async def create_filter(
    config: FilterConfig,
    session_id: Optional[str] = None,
    cache: Redis = Depends(depends_redis),
) -> Dict:
    """ Define a new filter configuration (data operation) """

    filter_id = IDPREDIX + str(uuid4())

    await cache.set(filter_id, config.json())
    if session_id:
        await _update_session_list_item(session_id, 'filter_info', [filter_id], cache)
    return dict(filter_id=filter_id)


@router.get('/{filter_id}')
async def get_filter(
    filter_id: str,
    session_id: Optional[str] = None,
    cache: Redis = Depends(depends_redis),
) -> Dict:
    """ Run and return data from a   filter (data operation) """

    filter_info_json = json.loads(await cache.get(filter_id))
    filter_info = FilterConfig(**filter_info_json)

    filter_strategy = factory.create_filter_strategy(filter_info)
    result = filter_strategy.get(session_id)
    if result and session_id:
        await _update_session(session_id, result, cache)

    return result

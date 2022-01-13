"""
Data Source context
"""
import json
from typing import Dict, Optional
from uuid import uuid4

from aioredis import Redis
from fastapi import APIRouter, Depends
from fastapi_plugins import depends_redis

from oteapi.app.models.filterconfig import FilterConfig
from oteapi.app.strategy.ifilterstrategy import create_filter_strategy

from .session import _update_session, _update_session_list_item

router = APIRouter()

IDPREDIX = "filter-"


@router.post("/")
async def create_filter(
    config: FilterConfig,
    session_id: Optional[str] = None,
    cache: Redis = Depends(depends_redis),
) -> Dict:
    """Define a new filter configuration (data operation)"""

    filter_id = IDPREDIX + str(uuid4())

    await cache.set(filter_id, config.json())
    if session_id:
        await _update_session_list_item(session_id, "filter_info", [filter_id], cache)
    return dict(filter_id=filter_id)


@router.get("/{filter_id}")
async def get_filter(
    filter_id: str,
    session_id: Optional[str] = None,
    cache: Redis = Depends(depends_redis),
) -> Dict:
    """Run and return data from a   filter (data operation)"""

    filter_info_json = json.loads(await cache.get(filter_id))
    filter_info = FilterConfig(**filter_info_json)
    filter_strategy = create_filter_strategy(filter_info)
    session_data = None if not session_id else json.loads(await cache.get(session_id))
    result = filter_strategy.get(session_data)
    if result and session_id:
        await _update_session(session_id, result, cache)

    return result


@router.post("/{filter_id}/initialize")
async def initialize_filter(
    filter_id: str,
    session_id: Optional[str] = None,
    cache: Redis = Depends(depends_redis),
) -> Dict:
    """Initialize and return data to update session"""

    filter_info_json = json.loads(await cache.get(filter_id))
    filter_info = FilterConfig(**filter_info_json)
    filter_strategy = create_filter_strategy(filter_info)
    session_data = None if not session_id else json.loads(await cache.get(session_id))
    result = filter_strategy.initialize(session_data)
    if result and session_id:
        await _update_session(session_id, result, cache)

    return result

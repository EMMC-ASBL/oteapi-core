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
from app.strategy import factory
from app.models.transformationconfig import TransformationConfig
from .session import _update_session, _update_session_list_item

router = APIRouter()

IDPREDIX = 'transformation-'


@router.post('/')
async def create_transformation(
    config: TransformationConfig,
    session_id: Optional[str] = None,
    cache: Redis = Depends(depends_redis),
) -> Dict:
    """ Create a new transformation configuration """
    transformation_id = IDPREDIX + str(uuid4())

    await cache.set(transformation_id, config.json())
    if session_id:
        await _update_session_list_item(session_id, 'transformation_info', [transformation_id], cache)
    return dict(transformation_id=transformation_id)

@router.get('/{transformation_id}/status')
async def get_transformation_status(
    transformation_id: str,
    cache: Redis = Depends(depends_redis),
) -> Dict:
    # Fetch transformation info from cache and populate the pydantic model
    transformation_info_json = json.loads(await cache.get(transformation_id))
    transformation_info = TransformationConfig(**transformation_info_json)

    # Apply the appropriate transformation strategy (plugin) using the factory
    transformation_strategy = factory.create_transformation_strategy(transformation_info)

    status = transformation_strategy.status()
    return status

@router.get('/{transformation_id}')
async def get_transformation(
    transformation_id: str,
    session_id: Optional[str] = None,
    cache: Redis = Depends(depends_redis),
) -> Dict:
    # Fetch transformation info from cache and populate the pydantic model
    transformation_info_json = json.loads(await cache.get(transformation_id))
    transformation_info = TransformationConfig(**transformation_info_json)

    # Apply the appropriate transformation strategy (plugin) using the factory
    transformation_strategy = factory.create_transformation_strategy(transformation_info)

    result = transformation_strategy.get(session_id)
    if result and session_id:
        await _update_session(session_id, result, cache)

    return result

@router.post('/{transformation_id}/execute')
async def execute_transformation(
    transformation_id: str,
    session_id: Optional[str] = None,
    cache: Redis = Depends(depends_redis),
) -> Dict:
    # Fetch transformation info from cache
    transformation_info = json.loads(await cache.get(transformation_id))

    # Apply the appropriate transformation strategy (plugin) using the factory
    transformation_strategy = factory.create_transformation_strategy(TransformationConfig(**transformation_info))

    # If session id is given, pass the object to the strategy create function
    if session_id:
        session_data = json.loads(await cache.get(session_id))
        create_result = transformation_strategy.create(session_data)
    else:
        create_result = transformation_strategy.create()
    await _update_session(session_id, create_result, cache)
    jobid = transformation_strategy.run()
    if session_id:
        await _update_session_list_item(session_id, 'jobs', [(jobid, transformation_id)], cache)

    return dict(jobid=jobid)

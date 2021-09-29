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

IDPREDIX = 'transformation-'

class TranformationConfig(BaseModel):
    app_type: str
    configuration: Optional[Dict]


@router.post('/')
async def create_transformation(
    config: TranformationConfig,
    session_id: Optional[str] = None,
    cache: Redis = Depends(depends_redis),
) -> Dict:
    transformation_id = IDPREDIX + str(uuid4())
    transformation_info = {
        'app_type': config.app_type,
        'configuration': config.configuration
    }

    await cache.set(transformation_id, json.dumps(transformation_info).encode('utf-8'))
    if session_id:
        await _update_session_list_item(session_id, 'transformation_info', [transformation_id], cache)
    return {'transformation_id': transformation_id}


@router.post('/{transformation_id}/execute')
async def execute_transformation(
    transformation_id: str,
    session_id: Optional[str] = None,
    cache: Redis = Depends(depends_redis),
) -> Dict:
    # Fetch transformation info from cache
    transformation_info = json.loads(await cache.get(transformation_id))

    # Apply the appropriate transformation strategy (plugin) using the factory
    transformation_strategy = factory.create_transformation_strategy(transformation_info)

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

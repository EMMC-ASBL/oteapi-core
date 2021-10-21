"""
Data Source context
"""
from uuid import uuid4
import json

from typing import Dict, Optional
from fastapi import APIRouter, Depends
from fastapi_plugins import depends_redis
from aioredis import Redis
from app.models.transformationconfig import TransformationConfig
from app.strategy.itransformationstrategy import create_transformation_strategy
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
        await _update_session_list_item(
            session_id,
            'transformation_info',
            [transformation_id],
            cache)
    return dict(transformation_id=transformation_id)

@router.get('/{transformation_id}/status')
async def get_transformation_status(
    transformation_id: str,
    cache: Redis = Depends(depends_redis),
) -> Dict:
    """ Get the current status of a defined transformation """
    # Fetch transformation info from cache and populate the pydantic model
    transformation_info_json = json.loads(await cache.get(transformation_id))
    transformation_info = TransformationConfig(**transformation_info_json)

    # Apply the appropriate transformation strategy (plugin) using the factory
    transformation_strategy = create_transformation_strategy(transformation_info)

    status = transformation_strategy.status()
    return status

@router.get('/{transformation_id}')
async def get_transformation(
    transformation_id: str,
    session_id: Optional[str] = None,
    cache: Redis = Depends(depends_redis),
) -> Dict:
    """ Get transformation """

    # Fetch transformation info from cache and populate the pydantic model
    transformation_info_json = json.loads(await cache.get(transformation_id))
    transformation_info = TransformationConfig(**transformation_info_json)

    # Apply the appropriate transformation strategy (plugin) using the factory
    transformation_strategy = create_transformation_strategy(transformation_info)

    session_data = None if not session_id else json.loads(await cache.get(session_id))
    result = transformation_strategy.get(session_data)
    if result and session_id:
        await _update_session(session_id, result, cache)

    return result

@router.post('/{transformation_id}/execute')
async def execute_transformation(
    transformation_id: str,
    session_id: Optional[str] = None,
    cache: Redis = Depends(depends_redis),
) -> Dict:
    """ Execute (run) a transformation """
    # Fetch transformation info from cache
    transformation_info = json.loads(await cache.get(transformation_id))

    # Apply the appropriate transformation strategy (plugin) using the factory
    transformation_strategy = create_transformation_strategy(
        TransformationConfig(**transformation_info))

    # If session id is given, pass the object to the strategy create function
    session_data = None if not session_id else json.loads(await cache.get(session_id))
    run_result = transformation_strategy.run(session_data)

    if session_id and run_result:
        await _update_session(session_id, run_result, cache)

    return run_result

@router.post('/{transformation_id}/initialize')
async def initialize_transformation(
    transformation_id: str,
    session_id: Optional[str] = None,
    cache: Redis = Depends(depends_redis),
) -> Dict:
    """ Initialize a transformation """
    # Fetch transformation info from cache
    transformation_info = json.loads(await cache.get(transformation_id))

    # Apply the appropriate transformation strategy (plugin) using the factory
    transformation_strategy = create_transformation_strategy(
        TransformationConfig(**transformation_info))

    # If session id is given, pass the object to the strategy create function
    session_data = None if not session_id else json.loads(await cache.get(session_id))
    init_result = transformation_strategy.initialize(session_data)

    if session_id and init_result:
        await _update_session(session_id, init_result, cache)

    return init_result

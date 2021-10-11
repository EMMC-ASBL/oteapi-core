"""
Data Source context
"""
from typing import Dict, List, Optional, TypeVar
from uuid import uuid4
import json
from pydantic import BaseModel, AnyUrl
from fastapi import APIRouter, Depends
from fastapi_plugins import depends_redis
from aioredis import Redis
from app.strategy import factory
from urllib.parse import urlparse
from .session import _update_session, _update_session_list_item
from app.models.resourceconfig import ResourceConfig


router = APIRouter()

IDPREDIX = 'dataresource-'


@router.post('/')
async def create_dataresource(
    config: ResourceConfig,
    session_id: Optional[str] = None,
    cache: Redis = Depends(depends_redis),
) -> Dict:
    """ Register an external data resource. If the resource is a service the <b>accessURL</b> must be specified. (For instance landing page, SPARQL endpoints, etc.)"""
    resource_id = IDPREDIX + str(uuid4())

    await cache.set(resource_id, config.json())
    if session_id:
        await _update_session_list_item(session_id, 'resource_info', [resource_id], cache)
    return dict(resource_id=resource_id)


@router.get('/{resource_id}/info')
async def info_dataresource(
    resource_id: str,
    cache: Redis = Depends(depends_redis),
) -> Dict:
    """ Get data resource info """
    resource_info_json = json.loads(await cache.get(resource_id))
    resource_info = ResourceConfig(**resource_info_json)

    return resource_info.dict() #resource_info = resource_info)

@router.get('/{resource_id}')
async def get_dataresource(
    resource_id: str,
    session_id: Optional[str] = None,
    cache: Redis = Depends(depends_redis),
) -> Dict:
    """ Get data resource """
    resource_info_json = json.loads(await cache.get(resource_id))
    resource_config = ResourceConfig(**resource_info_json)
    strategy = factory.create_resource_strategy(resource_config)
    result = strategy.get(session_id)
    if result and session_id:
        await _update_session(session_id, result, cache)

    return result


@router.get('/{resource_id}/read')
async def read_dataresource(
    resource_id: str,
    session_id: Optional[str] = None,
    cache: Redis = Depends(depends_redis),
) -> Dict:
    """
    Read data from dataresource using the appropriate download strategy.
    Parse data information using the appropriate parser
    """
    resource_info_json = json.loads(await cache.get(resource_id))
    resource_config = ResourceConfig(**resource_info_json)
    session_data = {}
    if session_id:
        session_data = json.loads(await cache.get(session_id))
    # Download

    download_strategy = factory.create_download_strategy(resource_config)
    read_output = download_strategy.read(session_data)
    if session_id:
        await _update_session(session_id, read_output, cache)

    # Parse
    parse_strategy = factory.create_parse_strategy(resource_config)
    parse_output = parse_strategy.parse(session_data)
    if session_id:
        await _update_session(session_id, parse_output, cache)

    return {"status":"ok"}

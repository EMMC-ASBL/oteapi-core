"""
Data Source context
"""
import json
from typing import Dict, Optional
from uuid import uuid4

from aioredis import Redis
from fastapi import APIRouter, Depends, HTTPException
from fastapi_plugins import depends_redis

from oteapi.app.models.resourceconfig import ResourceConfig
from oteapi.app.strategy.idownloadstrategy import create_download_strategy
from oteapi.app.strategy.iparsestrategy import create_parse_strategy
from oteapi.app.strategy.iresourcestrategy import create_resource_strategy

from .session import _update_session, _update_session_list_item

router = APIRouter()

IDPREDIX = "dataresource-"


@router.post("/")
async def create_dataresource(
    config: ResourceConfig,
    session_id: Optional[str] = None,
    cache: Redis = Depends(depends_redis),
) -> Dict:
    """
    Register an external data resource.
    -----------------------------------

    An external data resource can be any data distribution provider
    that provides services of obtaining information through queries,
    REST APIs or other protocol, or directly downloadable artifacts
    (files) through data exchange procolols (such as sftp, https
    etc...)

    If the resource URL is as direct link to a downloadable file, set
    the downloadURL property, otherwise set the accessURL the service
    and specify the service name with the mediaType property.

    """
    resource_id = IDPREDIX + str(uuid4())

    await cache.set(resource_id, config.json())
    if session_id:
        await _update_session_list_item(
            session_id, "resource_info", [resource_id], cache
        )
    return dict(resource_id=resource_id)


@router.get("/{resource_id}/info")
async def info_dataresource(
    resource_id: str,
    cache: Redis = Depends(depends_redis),
) -> Dict:
    """Get data resource info"""
    resource_info_json = json.loads(await cache.get(resource_id))
    resource_info = ResourceConfig(**resource_info_json)

    return resource_info.dict()  # resource_info = resource_info)


@router.get("/{resource_id}/read")
@router.get("/{resource_id}")
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
    session_data = None if not session_id else json.loads(await cache.get(session_id))

    if resource_config.accessUrl and resource_config.accessService:
        strategy = create_resource_strategy(resource_config)
        session_data = (
            None if not session_id else json.loads(await cache.get(session_id))
        )
        output = strategy.get(session_data)
        if output and session_id:
            await _update_session(session_id, output, cache)
    elif resource_config.downloadUrl and resource_config.mediaType:
        download_strategy = create_download_strategy(resource_config)
        output = download_strategy.get(session_data)
        if session_id:
            await _update_session(session_id, output, cache)
            session_data = json.loads(await cache.get(session_id))
        # Parse
        parse_strategy = create_parse_strategy(resource_config)
        output = parse_strategy.parse(session_data)
        if session_id:
            await _update_session(session_id, output, cache)
    else:
        raise HTTPException(
            status_code=404,
            detail="Missing downloadUrl/mediaType or accessUrl/accessService identifier",
        )
    return output


@router.post("/{resource_id}/initialize")
async def initialize_dataresource(
    resource_id: str,
    session_id: Optional[str] = None,
    cache: Redis = Depends(depends_redis),
) -> Dict:
    """Initialize data resource"""

    resource_info_json = json.loads(await cache.get(resource_id))
    resource_config = ResourceConfig(**resource_info_json)

    if resource_config.accessUrl and resource_config.accessService:
        strategy = create_resource_strategy(resource_config)
    elif resource_config.downloadUrl and resource_config.mediaType:
        strategy = create_download_strategy(resource_config)
    else:
        raise HTTPException(
            status_code=404,
            detail="Missing downloadUrl/mediaType or accessUrl/accessService identifier",
        )
    session_data = None if not session_id else json.loads(await cache.get(session_id))
    result = strategy.initialize(session_data)
    if result and session_id:
        await _update_session(session_id, result, cache)
    return result

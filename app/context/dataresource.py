"""
Data Source context
"""
from typing import Dict, Optional
from uuid import uuid4
import json
from fastapi import APIRouter, Depends, HTTPException
from fastapi_plugins import depends_redis
from aioredis import Redis
from app.strategy.idownloadstrategy import create_download_strategy
from app.strategy.iparsestrategy import create_parse_strategy
from app.strategy.iresourcestrategy import create_resource_strategy
from app.models.resourceconfig import ResourceConfig
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


@router.get("/{resource_id}")
async def get_dataresource(
    resource_id: str,
    session_id: Optional[str] = None,
    cache: Redis = Depends(depends_redis),
) -> Dict:
    """Get data resource"""

    resource_info_json = json.loads(await cache.get(resource_id))
    resource_config = ResourceConfig(**resource_info_json)

    if resource_config.accessUrl and resource_config.accessService:
        strategy = create_resource_strategy(resource_config)
        session_data = (
            None if not session_id else json.loads(await cache.get(session_id))
        )
        result = strategy.get(session_data)
    elif resource_config.downloadUrl and resource_config.mediaType:
        strategy = create_download_strategy(resource_config)
        session_data = (
            None if not session_id else json.loads(await cache.get(session_id))
        )
        result = strategy.get(session_data)
    else:
        raise HTTPException(
            status_code=404,
            detail="Missing downloadUrl/mediaType or accessUrl/accessService identifyer",
        )
    if result and session_id:
        await _update_session(session_id, result, cache)
    return result


@router.get("/{resource_id}/read")
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
        result = strategy.get(session_data)
        if result and session_id:
            await _update_session(session_id, result, cache)
    elif resource_config.downloadUrl and resource_config.mediaType:
        download_strategy = create_download_strategy(resource_config)
        read_output = download_strategy.read(session_data)
        if session_id:
            await _update_session(session_id, read_output, cache)
        # Parse
        parse_strategy = create_parse_strategy(resource_config)
        parse_output = parse_strategy.parse(session_data)
        if session_id:
            await _update_session(session_id, parse_output, cache)
        return {"status": "ok"}
    else:
        raise HTTPException(
            status_code=404,
            detail="Missing downloadUrl/mediaType or accessUrl/accessService identifyer",
        )


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
            detail="Missing downloadUrl/mediaType or accessUrl/accessService identifyer",
        )
    session_data = None if not session_id else json.loads(await cache.get(session_id))
    result = strategy.initialize(session_data)
    if result and session_id:
        await _update_session(session_id, result, cache)
    return result

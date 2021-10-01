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
from app import factory
from urllib.parse import urlparse
from .session import _update_session, _update_session_list_item
import dlite


router = APIRouter()

IDPREDIX = 'dataresource-'

class ResourceConfig(BaseModel):
    downloadUrl: AnyUrl
    mediaType: str
    accessUrl: Optional[str] # doc
    license: Optional[str]
    accessRights: Optional [str]
    description: Optional [str]
    published: Optional [str]
    configuration: Optional[Dict]

class ResourceInfo(BaseModel):
    url: AnyUrl
    media_type: str
    configuration: Dict
    scheme: str
    path: str
    username: Optional[str] = None
    password: Optional[str] = None
    hostname: Optional[str] = None
    port: Optional[int] = None


@router.post('/')
async def create_dataresource(
    config: ResourceConfig,
    session_id: Optional[str] = None,
    cache: Redis = Depends(depends_redis),
) -> Dict:
    """ Register an external data resource. If the resource is a service the <b>accessURL</b> must be specified. (For instance landing page, SPARQL endpoints, etc.)"""
    resource_id = IDPREDIX + str(uuid4())

    resource_info = ResourceInfo(
        url=config.downloadUrl,
        media_type=config.mediaType,
        configuration=config.configuration,
        scheme=config.downloadUrl.scheme,
        path=config.downloadUrl.path,
        username=config.downloadUrl.user,
        password=config.downloadUrl.password,
        hostname=config.downloadUrl.host,
        port=config.downloadUrl.port)
    print (resource_info.dict())

    await cache.set(resource_id, resource_info.json())
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
    resource_info = ResourceInfo(**resource_info_json)

    return resource_info.dict() #resource_info = resource_info)


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
    resource_info = json.loads(await cache.get(resource_id))

    # Download
    download_strategy = factory.create_download_strategy(resource_info)
    read_output = download_strategy.read()
    if session_id:
        await _update_session(session_id, read_output, cache)

    # Parse
    parse_strategy = factory.create_parse_strategy(resource_info)
    parse_output = parse_strategy.parse()
    if session_id:
        await _update_session(session_id, parse_output, cache)

    return {"status":"ok"}

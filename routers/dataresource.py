from fastapi import APIRouter
from fastapi import FastAPI, Depends
from abc import ABC, abstractmethod
from typing import Optional, Dict
from urllib.parse import urlparse
from soft.dataspace.dataspace import Dataspace
from pydantic import BaseModel
from uuid import uuid4
from ontotrans.datasource import DataSourceContext
from routers import test

import json
import fastapi_plugins
import aioredis
import pandas as pd
import requests
import pysftp

router = APIRouter()

class ResourceConfig(BaseModel):
    downloadUrl: str
    mediaType: str


@router.get('/')
async def show_dataresource():
    return 'hello'

@router.post('/')
async def create_dataresource(
    config: ResourceConfig,
    cache: aioredis.Redis=Depends(fastapi_plugins.depends_redis),    
) -> Dict:
    resource_id = str(uuid4())
    o = urlparse(config.downloadUrl)
    resource_info = {
        'uri': config.downloadUrl,
        'media_type': config.mediaType,
        'scheme': o.scheme,
        'netloc': o.netloc,
        'path': o.path,
        'username': o.username,
        'password': o.password,
        'hostname': o.hostname,
        'port': o.port,
        
    }
    await cache.set(resource_id, json.dumps(resource_info).encode('utf-8'))
    return dict(resource_id=resource_id,
        resource_info=resource_info)

@router.get('/{resource_id}')
async def info_dataresource(
    resource_id: str,
    cache: aioredis.Redis=Depends(fastapi_plugins.depends_redis),    
    ) -> Dict:
    return json.loads(await cache.get(resource_id))

@router.get('/{resource_id}/read')
async def read_dataresource(
    resource_id: str,
    cache: aioredis.Redis=Depends(fastapi_plugins.depends_redis),    
    ) -> Dict:
    resource_info = json.loads(await cache.get(resource_id))

    ctx = DataSourceContext(resource_info['uri'], resource_info['media_type'])
    content = ctx.read()
    
    return json.loads(content.to_json())

@router.get('/{resource_id}/datamodel')
async def datamodel_dataresource(
    resource_id: str,
    cache: aioredis.Redis=Depends(fastapi_plugins.depends_redis),    
    ) -> Dict:
    resource_info = json.loads(await cache.get(resource_id))
    ctx = DataSourceContext(resource_info['uri'], resource_info['media_type'])
    content = ctx.datamodel()
    return content
    

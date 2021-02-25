from fastapi import APIRouter, Depends
from fastapi import FastAPI
from abc import ABC, abstractmethod
from typing import Optional, Dict
from pydantic import BaseModel
from uuid import uuid4
import json
import fastapi_plugins
import aioredis
from tasks import command, read
import requests
import http3

router = APIRouter()
client = http3.AsyncClient()

class PipeConfig(BaseModel):
    filterUrl: str

@router.post("/")
async def create_pipe(
    config: PipeConfig,
    cache: aioredis.Redis = Depends(fastapi_plugins.depends_redis),
) -> Dict:
    pipe_id = str(uuid4())
    pipe_info = {
        'filter_url': config.filterUrl,
    }
    await cache.set(pipe_id, json.dumps(pipe_info).encode('utf-8'))
    return dict(pipe_id=pipe_id)


# return data
@router.get("/{pipe_id}")
async def data_pipe(
    pipe_id: str,
    cache: aioredis.Redis = Depends(fastapi_plugins.depends_redis),
) -> Dict:
    pipe_info = json.loads(await cache.get(pipe_id))
    
    filterUrl = pipe_info['filter_url']
    # uri = f'http://ontoapi:8000/dataresource/{sourceId}/read'

    response = await client.get(filterUrl)
    return json.loads(response.text)


# same as @router.get("/{pipe_id}")
# @router.get("/{pipe_id}/data")
# async def info_mapping():
#     return ' '

@router.get("/")
async def show_pipe():
    return ' '

@router.put("/{pipe_id}/flush")
async def read_pipe():
    return ' '

@router.delete("/{pipe_id}") 
async def delete_pipe():
    return ' '

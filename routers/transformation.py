from fastapi import APIRouter, Depends
from fastapi import FastAPI, Depends
from abc import ABC, abstractmethod
from typing import Optional, Dict
from pydantic import BaseModel
from uuid import uuid4
from ontotrans.transformation import TransformationContext
import json
import fastapi_plugins
import aioredis
import requests
import http3
import json
client = http3.AsyncClient()

router = APIRouter()


class TransformationConfig(BaseModel):
    applicationName: str
    applicationType: str

# Instantiate a transformation
@router.post("/")
async def create_transformation(
    config: TransformationConfig,
    cache: aioredis.Redis = Depends(fastapi_plugins.depends_redis),
) -> Dict:
    transformation_id = str(uuid4())
    transformation_info = {
        'application_name': config.applicationName,
        'application_type': config.applicationType
    }
    await cache.set(transformation_id, json.dumps(transformation_info).encode('utf-8'))
    return dict(transformation_id=transformation_id)


# Add a pipe to get data/ info
@router.post("/{transformation_id}/setpipe")
async def add_pipe_transformation(
    transformation_id: str,
    pipe_url: str,
    cache: aioredis.Redis = Depends(fastapi_plugins.depends_redis),
) -> Dict:
    transformation_info = json.loads(await cache.get(transformation_id))
    transformation_info = {
        'application_name':  transformation_info['application_name'],
        'application_type':  transformation_info['application_type'],
        'pipe_url': pipe_url,
    }
    await cache.set(transformation_id, json.dumps(transformation_info).encode('utf-8'))
    return 'pipe added'

# Run a transformation
@router.post("/{transformation_id}/run")
async def run_transformation(
    transformation_id: str,
    cache: aioredis.Redis = Depends(fastapi_plugins.depends_redis),
) -> Dict:
    transformation_info = json.loads(await cache.get(transformation_id))
    pipe_url = transformation_info['pipe_url']
    transformationctx = TransformationContext(
        transformation_info['application_name'], transformation_info['application_type'])
    
    response = await client.get(pipe_url)
    transformationctx.write(response.text)
    return 'Transformation complete'

# returns transformation details
@ router.get("/{transformation_id}/ref")
async def info_transformation(
    transformation_id: str,
    cache: aioredis.Redis = Depends(fastapi_plugins.depends_redis),
) -> Dict:
    return json.loads(await cache.get(transformation_id))


@router.get("/{transformation_id}")
async def status_transformation():
    return ' '


@router.get("/")
async def show_transformation():
    return ' '


@ router.delete("/{transformation_id}")
async def delete_transformation():
    return ' '

from fastapi import APIRouter
from fastapi import FastAPI, Depends, BackgroundTasks
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
import subprocess
import os
from tasks import command

router = APIRouter()


class TransformationConfig(BaseModel):
    applicationName: str
    applicationType: str

#run endpoint 
#addon for pipeid 

@router.post("/")
async def create_transformation(config: TransformationConfig,
                                background_tasks: BackgroundTasks,
                                cache: aioredis.Redis = Depends(
                                    fastapi_plugins.depends_redis),
                                ) -> Dict:
    transformation_id = str(uuid4())
    transformation_info = {
        'application_name': config.applicationName,
        'application_type': config.applicationType
    }
    # to run
    await cache.set(transformation_id, json.dumps(transformation_info).encode('utf-8'))
    try:
        command.delay(config.applicationName)
    except Exception as e:
        print(e)

    return dict(transformation_id=transformation_id)

# connecting to a trans--starts and returns id
# new transformation --id, run on id --new id for specfic run


@router.get("/")
async def show_transformation():
    return ' '


@router.get("/{transformation_id}")
async def status_transformation():
    # return someoutput
    return ' '

@router.post("/{transformation_id}/add")
async def addPipe_transformation():
    # return someoutput
    return ' '

@router.post("/{transformation_id}/run")
async def run_transformation():
    # command.delay(config.applicationName)
    return ' '

@router.delete("/{transformation_id}")
async def delete_transformation():
    return ' '


@router.get("/{transformation_id}/ref")
async def info_transformation(
    transformation_id: str,
    cache: aioredis.Redis = Depends(fastapi_plugins.depends_redis),
) -> Dict:
    return json.loads(await cache.get(transformation_id))

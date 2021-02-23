from fastapi import FastAPI, Depends
from abc import ABC, abstractmethod
from typing import Optional, Dict
from urllib.parse import urlparse
from soft.dataspace.dataspace import Dataspace
from pydantic import BaseModel
from uuid import uuid4
from ontotrans.datasource import DataSourceContext
from routers import test, dataresource

import json
import fastapi_plugins
import aioredis
import pandas as pd
import requests
import pysftp

class AppSettings(fastapi_plugins.RedisSettings):
    api_name: str = str(__name__)

app = FastAPI()
config = AppSettings()
app.include_router(test.router, prefix="/test")
app.include_router(dataresource.router, prefix="/dataresource")


@app.get('/')
async def root_get(
    cache: aioredis.Redis=Depends(fastapi_plugins.depends_redis),
) -> Dict:
    return dict(ping=await cache.ping())


@app.on_event('startup')
async def on_startup() -> None:
    await fastapi_plugins.redis_plugin.init_app(app, config=config)
    await fastapi_plugins.redis_plugin.init()


@app.on_event('shutdown')
async def on_shutdown() -> None:
    await fastapi_plugins.redis_plugin.terminate()

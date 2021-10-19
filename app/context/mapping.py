"""
Data Source context
"""
from uuid import uuid4
import json
from typing import Optional, Dict
from fastapi import APIRouter, Depends
from fastapi_plugins import depends_redis
from aioredis import Redis
from app.strategy import factory
from app.models.mappingconfig import MappingConfig
from .session import _update_session, _update_session_list_item


router = APIRouter()

IDPREDIX = 'mapping-'


@router.post('/')
async def create_mapping(
    config: MappingConfig,
    session_id: Optional[str] = None,
    cache: Redis = Depends(depends_redis),
) -> Dict:
    """ Define a new mapping configuration (ontological representation)
    Mapping (ontology alignment), is the process of defining
    relationships between concepts in ontologies.
    """
    mapping_id = IDPREDIX + str(uuid4())

    await cache.set(mapping_id, config.json())
    if session_id:
        await _update_session_list_item(session_id, 'mapping_info', [mapping_id], cache)
    return dict(mapping_id=mapping_id)


@router.get('/{mapping_id}')
async def get_mapping(
    mapping_id: str,
    session_id: Optional[str] = None,
    cache: Redis = Depends(depends_redis),
) -> Dict:
    """ Run and return data """
    mapping_info_json = json.loads(await cache.get(mapping_id))
    mapping_info = MappingConfig(**mapping_info_json)

    mapping_strategy = factory.create_mapping_strategy(mapping_info)
    result = mapping_strategy.get(session_id)
    if result and session_id:
        await _update_session(session_id, result, cache)

    return result

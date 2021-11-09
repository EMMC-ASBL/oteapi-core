"""
Data Source context
"""
from uuid import uuid4
import json
from typing import Optional, Dict
from fastapi import APIRouter, Depends
from fastapi_plugins import depends_redis
from aioredis import Redis
from app.models.mappingconfig import MappingConfig
from app.strategy.imappingstrategy import create_mapping_strategy
from .session import _update_session, _update_session_list_item


router = APIRouter()

IDPREDIX = "mapping-"


@router.post("/")
async def create_mapping(
    config: MappingConfig,
    session_id: Optional[str] = None,
    cache: Redis = Depends(depends_redis),
) -> Dict:
    """Define a new mapping configuration (ontological representation)
    Mapping (ontology alignment), is the process of defining
    relationships between concepts in ontologies.
    """
    mapping_id = IDPREDIX + str(uuid4())

    await cache.set(mapping_id, config.json())
    if session_id:
        await _update_session_list_item(session_id, "mapping_info", [mapping_id], cache)
    return dict(mapping_id=mapping_id)


@router.get("/{mapping_id}")
async def get_mapping(
    mapping_id: str,
    session_id: Optional[str] = None,
    cache: Redis = Depends(depends_redis),
) -> Dict:
    """Run and return data"""
    mapping_info_json = json.loads(await cache.get(mapping_id))
    mapping_info = MappingConfig(**mapping_info_json)

    mapping_strategy = create_mapping_strategy(mapping_info)
    session_data = None if not session_id else json.loads(await cache.get(session_id))
    result = mapping_strategy.get(session_data)
    if result and session_id:
        await _update_session(session_id, result, cache)

    return result


@router.post("/{mapping_id}/initialize")
async def initialize_mapping(
    mapping_id: str,
    session_id: Optional[str] = None,
    cache: Redis = Depends(depends_redis),
) -> Dict:
    """Initialize and update session"""
    mapping_info_json = json.loads(await cache.get(mapping_id))
    mapping_info = MappingConfig(**mapping_info_json)

    mapping_strategy = create_mapping_strategy(mapping_info)
    session_data = None if not session_id else json.loads(await cache.get(session_id))
    result = mapping_strategy.initialize(session_data)
    if result and session_id:
        await _update_session(session_id, result, cache)

    return result

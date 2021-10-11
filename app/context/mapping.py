"""
Data Source context
"""
from uuid import uuid4
import json

from fastapi import APIRouter, Depends
from fastapi_plugins import depends_redis
from aioredis import Redis
from typing import Optional, Dict
from app.strategy import factory
from app.models.mappingconfig import MappingConfig
from .session import _update_session, _update_session_list_item
import dlite


router = APIRouter()

IDPREDIX = 'Mapping-'


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
    return dict(status='ok')


@router.get('/{mapping_id}')
async def get_mapping(
    mapping_id: str,
    session_id: Optional[str] = None,
    cache: Redis = Depends(depends_redis),
) -> Dict:
    """ Run and return data """
    return dict(status='ok')

"""
Microservice Session
"""
from typing import Any, Dict, List
from uuid import uuid4
import json
from fastapi import APIRouter, Depends
from fastapi_plugins import depends_redis
from aioredis import Redis


router = APIRouter()

IDPREFIX = 'session-'

@router.post('/')
async def create_session(
    session: Dict[str, Any],
    cache: Redis = Depends(depends_redis),
) -> Dict[str,str]:
    """
    Create a new session
    --------------------

    The session allows for storing keyword/value pairs of information
    on the OTE server. The session can be shared between different OTE
    microservices.

    Attributes
    ----------
    - session : Dict[str,Any]
        A key/value object to be created as a session object
    - cache : Redis
        The in-memory storage engine to be used (default Redis)


    Return
    ------
    - session identifier : Dict[str,str]
        Object containing the session identifier

    """

    session_id = f'{IDPREFIX}{str(uuid4())}'
    new_session = session.copy()
    await cache.set(session_id, json.dumps(new_session).encode('utf-8'))
    return {'session_id': session_id}


@router.get('/')
async def list_sessions(
    cache: Redis = Depends(depends_redis),
) -> Dict[str,List[str]]:
    """ Get all session keys """
    keylist = []
    for key in await cache.keys(pattern=f'{IDPREFIX}*'):
        keylist.append(key)
    return dict(keys=keylist)


@router.delete('/')
async def delete_all_sessions(
    cache: Redis = Depends(depends_redis),
) -> Dict[str,str]:
    """ Delete all session keys

    WARNING: Data stored in sessions cannot be recovered after
    calling this endpoint.
    """
    keylist = await cache.keys(pattern=f'{IDPREFIX}*')

    await cache.delete(*keylist)
    return dict(status='ok', number_of_deleted_rows=len(keylist))


async def _get_session(
    session_id: str,
    redis: Redis = Depends(depends_redis),
) -> Dict:
    """ Return the session contents given a session_id """
    session = json.loads(await redis.get(session_id))
    return session

async def _update_session(
    session_id: str,
    updated_session: Dict[str, Any],
    redis: Redis,
) -> Dict:
    """ Update an existing session (to be called internally). """
    session = json.loads(await redis.get(session_id))
    session.update(updated_session)
    await redis.set(session_id, json.dumps(session).encode('utf-8'))
    return session

async def _update_session_list_item(
    session_id: str,
    list_key: str,
    list_items: List[Any],
    redis: Redis,
) -> Dict:
    """ Append or create list items to an existing session """
    session = json.loads(await redis.get(session_id))
    if list_key in session:
        session[list_key].append(list_items)
    else:
        session[list_key] = list_items
    await redis.set(session_id, json.dumps(session).encode('utf-8'))
    return session


@router.put('/{session_id}')
async def update_session(
    session_id: str,
    updatet_session: Dict[str, Any],
    cache: Redis = Depends(depends_redis),
) -> Dict:
    """ Update session object """
    session = json.loads(await cache.get(session_id))
    session.update(updatet_session)
    await cache.set(session_id, json.dumps(session).encode('utf-8'))
    return session


@router.get('/{session_id}')
async def get_session(
    session_id: str,
    cache: Redis = Depends(depends_redis),
) -> Dict:
    """ Fetch the entire session object """
    session = json.loads(await cache.get(session_id))
    return session


@router.delete('/{session_id}')
async def delete_session(
    session_id: str,
    cache: Redis = Depends(depends_redis),
) -> Dict:
    """ Delete a session object """
    await cache.delete(session_id)
    return dict(status = "ok")

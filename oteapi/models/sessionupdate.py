"""Pydantic SessionUpdate Data Model."""
from typing import Optional, Any, Dict

from pydantic import Field

from oteapi.models.genericconfig import AttrDict


class SessionUpdate(AttrDict):
    """Session Update Data Model for returning values."""

    
    

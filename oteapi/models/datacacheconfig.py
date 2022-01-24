"""Pydantic DataCache Configuration Data Model."""
from pathlib import Path

from pydantic import BaseModel, Field


class DataCacheConfig(BaseModel):
    """DataCache Configuration."""

    cacheDir: Path = Field("oteapi", description="Cache directory.")
    accessKey: str = Field(
        None,
        description="Key with which the downloaded content can be accessed. "
        "Should preferable be the hash (corresponding to `hashType`) of the "
        "content if it is known.",
    )
    hashType: str = Field(
        "md5",
        description="Hash algorithm to use for creating hash keys for stored "
        "data. Can be any algorithm supported by hashlib.",
    )
    expireTime: int = Field(
        3600 * 24 * 14,
        description="Number of seconds before the cache entry expires. "
        "Zero means no expiration. Default is two weeks.",
    )
    tag: str = Field(
        None,
        description="Tag assigned to the downloaded content, typically "
        "identifying a session. Used with the `evict()` method to clean up a "
        "all cache entries with a given tag.",
    )

"""Pydantic DataCache Configuration Data Model."""

from __future__ import annotations

from pathlib import Path

from pydantic import Field

from oteapi.models.genericconfig import AttrDict


class DataCacheConfig(AttrDict):
    """DataCache Configuration.

    This class should not be used directly as a configuration object
    for a strategy object, but only as a configuration field inside
    a configuration object.
    """

    cacheDir: Path = Field(Path("oteapi"), description="Cache directory.")
    accessKey: str | None = Field(
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
    tag: str | None = Field(
        None,
        description="Tag assigned to the downloaded content, typically "
        "identifying a session. Used with the `evict()` method to clean up a "
        "all cache entries with a given tag.",
    )

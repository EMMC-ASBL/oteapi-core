"""
Pydantic Download Configuration Data Model shared by most download strategies.
"""
from pathlib import Path

from pydantic import BaseModel, Field


class DownloadConfig(BaseModel):
    """Download Specific Data Configuration"""

    cacheDir: Path = Field(
        "{tmp}/oteapi",
        description="Cache directory.  `{tmp}` is substituted with the "
        "system temporary directory.",
    )
    accessKey: str = Field(
        None,
        description="Key with which the downloaded content can be accessed.  "
        "Should preferable be the hash (corresponding to hashType) of the "
        "content if it is known.",
    )
    hashType: str = Field(
        "md5",
        description="Hash algorithm to use for creating hash keys for stored "
        "data.  Can be any algorithm supported by hashlib.",
    )
    expireTime: int = Field(
        3600 * 24 * 14,
        description="Number of seconds before the cache entry expires.  "
        "Zero means no expiration.  Default is two weeks.",
    )
    tag: str = Field(
        None,
        description="Tag assigned to the downloaded content, typically "
        "identifying a session.  Used with the evict() method to clean up a "
        "all cache entries with a given tag.",
    )

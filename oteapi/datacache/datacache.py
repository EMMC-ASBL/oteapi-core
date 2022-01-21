"""Data cache based on DiskCache.
See https://github.com/grantjenks/python-diskcache

Features:
- persistent cache between sessions
- default keys are hashes of the stored data
- works with asyncio
- automatic expiration of cached data
- sessions can selectively be cleaned up via tags
- store small values in SQLite database and large values in files
- underlying library is actively developed and tested on Linux, Mac and Windows
- high performance

"""
import asyncio
import hashlib
import json
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import TYPE_CHECKING

from diskcache import Cache as DiskCache
from pydantic import Extra

from oteapi.models import DownloadConfig

if TYPE_CHECKING:
    from typing import Any, Iterator, Optional, Type, Union


def gethash(
    value: "Any",
    hashtype: str = "sha256",
    encoding: str = "utf-8",
    json_encoder: "Optional[Type[json.JSONEncoder]]" = None,
) -> str:
    """Return a hash of `value`.

    Can hash most python objects. Bytes and bytearrays are hashed directly.
    Strings are converted to bytes with the given encoding.
    All other objects are first serialised using json.

    Args:
        value: Value to hash.
        hashtype: Any of the hash algorithms supported by hashlib.
        encoding: Encoding used to convert strings to bytes before
            calculating the hash.
        json_encoder: Customised json encoder for complex Python objects.

    """
    if isinstance(value, (bytes, bytearray)):
        data = value
    elif isinstance(value, str):
        data = value.encode(encoding)
    else:
        # Try to serialise using json
        data = json.dumps(
            value,
            ensure_ascii=False,
            cls=json_encoder,
            sort_keys=True,
        ).encode(encoding)

    hash_ = hashlib.new(hashtype)
    hash_.update(data)
    return hash_.hexdigest()


def asyncrun(func, *args) -> "Any":
    """Runs `func` in a async thread-pool."""
    # Adds support for asyncio.
    # See http://www.grantjenks.com/docs/diskcache/tutorial.html#id13
    async def async_func(args):
        loop = asyncio.get_running_loop()
        future = loop.run_in_executor(None, func, *args)
        result = await future
        return result

    try:
        # Will raise a RuntimeError if there is no event loop
        asyncio.get_running_loop()
    except RuntimeError:
        # no event loop
        return asyncio.run(async_func(args))
    else:
        # within a running event loop
        return await func(*args)


class DataCache:
    """Initialise a cache instance with the given download configuration.

    Args:
        config: Download configurations.
        cache_dir: Cache directory overriding the config.

    Attributes:
        config: DownloadConfig instance.
        cache_dir: Subdirectory used for the Path to cache directory, e.g., `"my_oteapi"`.

    """

    def __init__(
        self,
        config: "Union[DownloadConfig, dict]" = None,
        cache_dir: "Optional[Union[Path, str]]" = None,
    ) -> None:
        if config is None:
            self.config = DownloadConfig()
        elif isinstance(config, dict):
            self.config = DownloadConfig(**config, extra=Extra.ignore)
        elif isinstance(config, DownloadConfig):
            self.config = config
        else:
            raise TypeError(config)

        if not cache_dir:
            cache_dir = self.config.cacheDir
        if isinstance(cache_dir, str):
            cache_dir = Path(cache_dir)
        if cache_dir.is_absolute():
            self.cache_dir = cache_dir
        else:
            self.cache_dir = Path(tempfile.gettempdir()).resolve() / cache_dir

        self.datacache = DiskCache(directory=self.cache_dir)

    def __contains__(self, key) -> bool:
        return key in self.datacache

    def __len__(self) -> int:
        return len(self.datacache)

    def __getitem__(self, key) -> "Any":
        return self.get(key)

    def __setitem__(self, key, value) -> None:
        self.add(value, key)

    def __delitem__(self, key) -> None:
        def deleter(key):
            del self.datacache[key]

        asyncrun(deleter, key)

    def __del__(self) -> None:
        def closer():
            self.datacache.expire()
            self.datacache.close()

        asyncrun(closer)

    def add(
        self,
        value: "Any",
        key: "Optional[str]" = None,
        expire: "Optional[int]" = None,
        tag: "Optional[str]" = None,
    ) -> str:
        """Add a value to cache.

        Existing value is overwritten if `key` is given and it already
        exists in the cache.

        Args:
            value: The value to add to the cache.
            key: If given, use this as the retrieval key.  Otherwise the key
                is either taken from the `accessKey` configuration or generated
                as a hash of `value`.
            expire: If given, the number of seconds before the value expire.
                Otherwise it is taken from the configuration.
            tag: Tag used with evict() for cleaning up a session.

        Returns:
            newkey: A key that can be used to retrieve `value` from cache
                later.

        """
        if not key:
            if self.config.accessKey:
                key = self.config.accessKey
            else:
                key = gethash(value, hashtype=self.config.hashType)
        if not expire:
            expire = self.config.expireTime

        # Needed because asyncio.run() does not support keyword arguments
        def setter(key, value, expire, tag):
            self.datacache.set(key, value, expire=expire, tag=tag)

        asyncrun(setter, key, value, expire, tag)

        return key

    def get(self, key: str) -> "Any":
        """Return the value corresponding to key."""
        if key not in self.datacache:
            raise KeyError(key)
        return asyncrun(self.datacache.get, key)

    @contextmanager
    def getfile(  # pylint: disable=too-many-arguments
        self,
        key: str,
        filename: "Optional[Union[Path, str]]" = None,
        prefix: "Optional[str]" = None,
        suffix: "Optional[str]" = None,
        directory: "Optional[str]" = None,
        delete: bool = True,
    ) -> "Iterator[Path]":
        """Write the value for `key` to file and return the filename.

        The file is created in the default directory for temporary
        files (which can be controlled by the TEMPDIR, TEMP or TMP
        environment variables). It is readable and writable only for
        the current user.

        This method is intended to be used in a `with` statement, to
        automatically delete the file when leaving the context.

        Example:

        ```python
        cache = DataCache()
        with cache.getfile('mykey') as filename:
            # do something with filename...
        # filename is deleted
        ```

        Args:
            key: Key of value to write to file
            filename: Full path to created file. If not given, a unique
                filename will be created.
            prefix: Prefix to prepend to the returned file name (default
                is "oteapi-download-").
            suffix: Suffix to append to the returned file name.
            directory: File directory if `filename` is None.
            delete: Whether to automatically delete created file when
                leaving the context.

        Returns:
            Path object of the created file.

        """
        if filename:
            filename = Path(filename).resolve()
            filename.write_bytes(self.get(key))
        else:
            if prefix is None:
                prefix = "oteapi-download-"
            with tempfile.NamedTemporaryFile(
                prefix=prefix, suffix=suffix, dir=directory, delete=False
            ) as handle:
                handle.write(self.get(key))
                filename = Path(handle.name).resolve()

        try:
            yield filename
        finally:
            if delete:
                filename.unlink()

    def evict(self, tag: str) -> None:
        """Remove all cache items with the given tag.

        Useful for cleaning up a session.
        """
        asyncrun(self.datacache.evict, tag)

    def clear(self) -> None:
        """Remove all items from cache."""
        asyncrun(self.datacache.clear)

# pylint: disable=R0913,W0613,C0103
"""
Data cache based on DiskCache
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
import os
import tempfile
from contextlib import contextmanager
from typing import Any, Union

from diskcache import Cache as DiskCache
from oteapi.app.models.downloadconfig import DownloadConfig  # pylint: disable=E0401
from pydantic import Extra


def gethash(
    value: Any,
    hashtype: str = "sha256",
    encoding="utf-8",
    json_encoder: json.JSONEncoder = None,
) -> str:
    """Return a hash of `value`.

    Args:
        value: Value to hash.
        hashtype: Any of the hash algorithms supported by hashlib.
        encoding: Encoding used to convert strings to bytes before
          calculating the hash.
        json_encoder: Customised json encoder for complex Python objects.

    Can hash most python objects.  Bytes and bytearray's are hashed
    directly.  Strings are converted to bytes with the given encoding.
    All other objects are first serialised using json.
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

    h = hashlib.new(hashtype)
    h.update(data)
    return h.hexdigest()


def asyncrun(func, *args):
    """Runs `func` in a async thread-pool."""
    # Adds support for asyncio.
    # See http://www.grantjenks.com/docs/diskcache/tutorial.html#id13
    async def async_func(args):
        loop = asyncio.get_running_loop()
        future = loop.run_in_executor(None, func, *args)
        result = await future
        return result

    return asyncio.run(async_func(args))


class DataCache:
    """Initialise a cache instance with the given download configuration.

    Args:
        config: Download configurations.
        cache_dir: Cache directory overriding the config.

    Attributes:
        config: DownloadConfig instance.
        cache_dir: Subdirectory used for teh Path to cache directory.
    """

    def __init__(
        self, config: Union[DownloadConfig, dict] = None, cache_dir: str = None
    ):
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
        self.cache_dir = cache_dir.format(tmp=tempfile.gettempdir())

        self.dc = DiskCache(directory=self.cache_dir)

    def __contains__(self, key):
        return key in self.dc

    def __len__(self):
        return len(self.dc)

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        self.add(value, key)

    def __delitem__(self, key):
        def deleter(key):
            del self.dc[key]

        asyncrun(deleter, key)

    def __del__(self):
        def closer():
            self.dc.expire()
            self.dc.close()

        asyncrun(closer)

    def add(
        self,
        value: Any,
        key: str = None,
        expire: int = None,
        tag: str = None,
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
            self.dc.set(key, value, expire=expire, tag=tag)

        asyncrun(setter, key, value, expire, tag)

        return key

    def get(self, key: str) -> Any:
        """Return the value corresponding to key."""
        if key not in self.dc:
            raise KeyError(key)
        return asyncrun(self.dc.get, key)

    @contextmanager
    def getfile(
        self,
        key: str,
        filename: str = None,
        prefix: str = None,
        suffix: str = None,
        directory: str = None,
        delete: bool = True,
    ) -> str:
        """Write the value for `key` to file and return the filename.

        Args:
            key: key of value to write to file
            filename: full path to created file.  If not given, a unique
              filename will be created.
            prefix: prefix to prepend to the returned file name (default
              is "oteapi-download-").
            suffix: suffix to append to the returned file name.
            directory: file directory if `filename` is None.
            delete: whether to automatically delete created file when
              leaving the context.

        Returns:
            Name of the created file.

        The file is created in the default directory for temporary
        files (which can be controlled by the TEMPDIR, TEMP or TMP
        environment variables).  It is readable and writable only for
        the current user.

        This method is intended to be used in a with statement, to
        automatically delete the file when leaving the context.

        Example:
        >>> cache = DataCache()
        >>> with cache.getfile('mykey') as filename:
        ...     # do something with filename...
        >>>
        >>> # filename is deleted
        """
        if filename:
            with open(filename, "rb") as f:
                f.write(self.get(key))
        else:
            if prefix is None:
                prefix = "oteapi-download-"
            with tempfile.NamedTemporaryFile(
                prefix=prefix, suffix=suffix, dir=directory, delete=False
            ) as f:
                f.write(self.get(key))
                filename = f.name

        try:
            yield filename
        finally:
            if delete:
                os.remove(filename)

    def evict(self, tag: str):
        """Remove all cache items with the given tag.

        Useful for cleaning up a session.
        """
        asyncrun(self.dc.evict, tag)

    def clear(self):
        """Remove all items from cache."""
        asyncrun(self.dc.clear)

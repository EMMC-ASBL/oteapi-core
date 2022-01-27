"""Tests for `oteapi.datacache.datacache`."""
# pylint: disable=unused-argument
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path


def test_cache(import_oteapi_modules, tmp_path: "Path") -> None:
    """Simple tests for the `DataCache`."""
    from oteapi.datacache.datacache import DataCache

    cache = DataCache(cache_dir=tmp_path / "oteapi-test_cache")

    val1 = b"a binary blob..."
    val2 = 42
    val3 = dict(a=[1, 2, 3], pi=3.14, s=set([0, "a"]))
    val4 = (1, 2, 3)

    key1 = cache.add(val1, tag="test_cache")
    key2 = cache.add(val2, tag="test_cache")
    key3 = cache.add(val3, key="a", tag="test_cache")
    key4 = cache.add(val4)

    assert cache[key1] == val1
    assert cache.get(key2) == val2
    assert cache.get(key3) == val3
    assert cache.get(key4) == val4

    assert len(cache) == 4
    del cache[key1]
    assert len(cache) == 3
    cache.evict("test_cache")
    assert len(cache) == 1
    cache.clear()
    assert len(cache) == 0

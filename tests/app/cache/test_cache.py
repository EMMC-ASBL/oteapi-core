import sys
from pathlib import Path

thisdir = Path(__file__).absolute().parent
sys.path.insert(1, str(thisdir.parent.parent.parent))

from oteapi.app.cache.cache import DataCache


def test_cache():
    cache = DataCache(cache_dir="{tmp}/oteapi-test_cache")

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

    assert len(cache) == 4
    del cache[key1]
    assert len(cache) == 3
    cache.evict("test_cache")
    assert len(cache) == 1
    cache.clear()
    assert len(cache) == 0

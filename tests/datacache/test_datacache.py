"""Tests for `oteapi.datacache.datacache`."""
# pylint: disable=invalid-name,import-error
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from pathlib import Path

    try:
        import ase
        import numpy
    except ImportError:
        pass


def test_cache(tmp_path: "Path") -> None:
    """Simple tests for the `DataCache`."""
    from oteapi.datacache import DataCache

    cache = DataCache(cache_dir=tmp_path / "oteapi-test_cache")

    val1 = b"a binary blob..."
    val2 = 42
    val3 = {"a": [1, 2, 3], "pi": 3.14, "s": (0, "a")}
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


def test_numpy(tmp_path: "Path") -> None:
    """Test adding numpy arrays to the datachache."""
    np: "numpy" = pytest.importorskip("numpy", reason="numpy is not installed")

    from oteapi.datacache import DataCache

    cache = DataCache(cache_dir=tmp_path / "oteapi-test_numpy")
    val = np.eye(4)
    key = cache.add(val)

    assert np.all(cache[key] == np.eye(4))
    cache.clear()


def test_ase_atoms(tmp_path: "Path") -> None:
    """Test adding ase Atoms objects to the datachache."""
    ase: "ase" = pytest.importorskip("ase", reason="ase is not installed")

    from ase.io.jsonio import MyEncoder

    from oteapi.datacache import DataCache

    cache = DataCache(cache_dir=tmp_path / "oteapi-test_numpy")
    atoms = ase.Atoms(
        symbols=[
            ase.Atom("H", [0.7575, 0.5871, 0.0]),
            ase.Atom("H", [-0.7575, 0.5871, 0.0]),
            ase.Atom("O", [0, 0, 0]),
        ],
    )
    key = cache.add(atoms, json_encoder=MyEncoder)

    atoms2: "ase.Atoms" = cache[key]
    assert len(atoms2) == 3
    assert atoms2.get_chemical_symbols() == ["H", "H", "O"]
    assert all(atoms2.positions[2] == (0, 0, 0))
    cache.clear()


def test_add_bind(tmp_path: "Path") -> None:
    """Test the `bind` argument to DataCache.add()."""
    from oteapi.datacache import DataCache

    cache = DataCache(cache_dir=tmp_path / "oteapi-add_bind")

    class Session(dict):
        pass

    session = Session()
    key = cache.add([1, 2, 3], bind=session)
    assert key in cache

    del session
    assert key not in cache

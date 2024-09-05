"""Tests the parse strategy for JSON."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path


def test_json(static_files: Path) -> None:
    """Test `application/json` parse strategy on local file."""
    import json

    from oteapi.strategies.parse.application_json import JSONDataParseStrategy

    sample_file = static_files / "sample2.json"
    config = {
        "parserType": "parser/json",
        "configuration": {
            "datacache_config": None,
            "downloadUrl": sample_file.as_uri(),
            "mediaType": "application/json",
        },
        "entity": "http://onto-ns.com/meta/0.4/example_iri",
    }
    parser = JSONDataParseStrategy(config)
    parser.initialize()

    test_data = json.loads(sample_file.read_text())

    assert parser.get().get("content", {}) == test_data

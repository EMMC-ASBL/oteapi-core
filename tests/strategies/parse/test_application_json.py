"""Tests the parse strategy for JSON."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

    from oteapi.interfaces import IParseStrategy


def test_json(static_files: "Path") -> None:
    """Test `application/json` parse strategy on local file."""
    import json

    from oteapi.strategies.parse.application_json import JSONDataParseStrategy,JSONConfig,JSONParserConfig

    sample_file = static_files / "sample2.json"

    config = {
        "downloadUrl": sample_file.as_uri(),
        "mediaType": "application/json",
    }
    parser: "IParseStrategy" = JSONDataParseStrategy(JSONParserConfig(
        parserType="parser/json",
        configuration=JSONConfig(datacache_config=None)
    ))
    parser.initialize()

    test_data = json.loads(sample_file.read_text())

    assert parser.get().content == test_data

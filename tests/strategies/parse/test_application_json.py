import json
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path


def test_json(static_files: "Path") -> None:
    """Test `application/json` parse strategy on local file."""
    from oteapi.strategies.parse.application_json import (
        JSONConfig,
        JSONDataParseStrategy,
        JSONParserConfig,
    )

    sample_file = static_files / "sample2.json"

    # Initialize the JSONDataParseStrategy with the appropriate configuration
    parser_config = JSONParserConfig(
        parserType="parser/json",
        configuration=JSONConfig(
            datacache_config=None, downloadUrl=sample_file.as_uri()
        ),
    )
    parser_strategy = JSONDataParseStrategy(parser_config)
    parser_strategy.initialize()

    # Read the sample file content and parse it as JSON
    with open(sample_file, "r") as file:
        expected_content = json.load(file)

    # Get the parsed content from the strategy
    parsed_content = parser_strategy.get().content

    # Assert that the parsed content matches the expected content
    assert parsed_content == expected_content

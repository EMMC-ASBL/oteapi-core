"""Tests the parse strategy for SQLite."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from pathlib import Path


sqlite_queries = [
    (
        "SELECT * FROM user_details WHERE user_details.user_id = 19;",
        (
            19,
            "jenny0988",
            "maria",
            "morgan",
            "Female",
            "ec9ed18ae2a13fef709964af24bb60e6",
            1,
        ),
    ),
    (
        "SELECT * FROM user_details WHERE user_details.user_id = 72;",
        (
            72,
            "brown84",
            "john",
            "ross",
            "Male",
            "738cb4da81a2790a9a845f902a811ea2",
            1,
        ),
    ),
]


@pytest.mark.parametrize(
    ("query", "expected"), sqlite_queries, ids=["configuration", "session"]
)
def test_sqlite(
    query: str,
    expected: tuple[int, str, str, str, str, str, int],
    static_files: Path,
) -> None:
    """Test `application/vnd.sqlite3` parse strategy on a local SQLite DB.

    Test both passing in the query as a configuration and through a session.
    """
    from oteapi.strategies.parse.application_vnd_sqlite import SqliteParseStrategy

    sample_file = static_files / "sample1.db"

    config = {
        "parserType": "parser/sqlite3",
        "entity": "http://onto-ns.com/meta/0.4/example_iri",
        "configuration": {
            "downloadUrl": sample_file.as_uri(),
            "mediaType": "application/vnd.sqlite3",
            "sqlquery": query,
        },
    }

    result = SqliteParseStrategy(parse_config=config).get()

    assert result["result"][0] == expected

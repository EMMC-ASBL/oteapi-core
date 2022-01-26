"""Tests the parse strategy for SQLite."""
from pathlib import Path


def test_sqlite(import_oteapi_modules):
    """Test `application/vnd.sqlite3` parse strategy on 'sample1.db',
    downloaded as SQL source 'sample1.sql' from filesamples.com.
    """
    from oteapi.models.resourceconfig import ResourceConfig
    from oteapi.strategies.parse.application_vnd_sqlite import SqliteParseStrategy

    filename = str((Path(__file__).resolve().parent / "sample1.db"))
    query1 = "SELECT * FROM user_details WHERE user_details.user_id = 19;"
    compare1 = (
        19,
        "jenny0988",
        "maria",
        "morgan",
        "Female",
        "ec9ed18ae2a13fef709964af24bb60e6",
        1,
    )
    query2 = "SELECT * FROM user_details WHERE user_details.user_id = 72;"
    compare2 = (
        72,
        "brown84",
        "john",
        "ross",
        "Male",
        "738cb4da81a2790a9a845f902a811ea2",
        1,
    )

    config = ResourceConfig(
        downloadUrl="file://dummy",
        mediaType="application/vnd.sqlite3",
    )

    parser = SqliteParseStrategy(config)
    reply1 = parser.parse({"filename": filename, "sqlquery": query1})
    reply2 = parser.parse({"filename": filename, "sqlquery": query2})

    assert reply1["result"][0] == compare1 and reply2["result"][0] == compare2

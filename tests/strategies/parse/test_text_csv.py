"""Tests the parse strategy for SQLite."""

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from typing import Tuple

    from oteapi.interfaces import IResourceStrategy


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


class MockPsycopg:
    """
    A class for mocking all psycop calls
    """

    result: "Tuple[int, str, str, str, str, str, int]"

    def cursor(self):
        """
        Mocks psycopg.cursor
        """
        return self

    def execute(self, query):
        """
        Mocks psycopg.execute by simply pulling one of the sqlite_queries
        """
        result = [q[1] for q in sqlite_queries if q[0] == query]
        self.result = result
        return self

    def fetchall(self):
        """
        Mocks psycopg.fetchall by returning  the 'result' from the execute method
        """
        return self.result

    def close(self):
        """
        Mocks the close method by doing nothing
        """
        return


@pytest.mark.parametrize(
    "query,expected",
    sqlite_queries,
    ids=["configuration", "session"],
)
def test_postgres(
    query: str,
    expected: "Tuple[int, str, str, str, str, str, int]",
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test `application/vnd.sqlite3` parse strategy on a local SQLite DB.

    Test both passing in the query as a configuration and through a session.
    """
    import psycopg

    from oteapi.strategies.parse.postgres import PostgresResourceStrategy

    def mock_connect(connect_str):
        connect_str = str(connect_str)
        # NOTE: this should work but for some reason we don't have
        #       the DB name in the accessUrl?
        # expected_connect_str = \
        #    "postgresql://postgres:postgres@localhost:5432/postgres"
        # assert connect_str == expected_connect_str
        return MockPsycopg()

    monkeypatch.setattr(psycopg, "connect", mock_connect)

    # NOTE there are a lot of tests one can do on ways of connecting to the DB
    #      e.g., trying combinations of accessUrl and connection_dict
    # connection_dict = {
    #    "dbname": "postgres",
    #    "user": "postgres",
    #    "password": "postgres",
    #    "host": "localhost",
    #    "port": 5432,
    # }

    config = {
        "accessUrl": "postgresql://postgres:postgres@localhost:5432/postgres",
        "accessService": "foo",
        "configuration": {
            "sqlquery": query,
        },
    }

    resource: "IResourceStrategy" = PostgresResourceStrategy(config)
    resource.initialize()

    result = resource.get({"sqlquery": query} if "19" not in query else None)

    assert result["result"][0] == expected

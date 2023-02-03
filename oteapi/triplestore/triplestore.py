"""
An RDF triplestore using Allegrograph
https://franz.com/agraph/support/documentation/current/python/api.html
https://franz.com/agraph/support/documentation/current/agraph-introduction.html

Features:

- Store mapping data (triple format)
- AllegroGraph has a well documented python API package

"""
# pylint: disable=too-many-arguments
from typing import TYPE_CHECKING

from franz.miniclient.request import RequestError
from franz.openrdf.connect import ag_connect
from franz.openrdf.rio.tupleformat import TupleFormat
from franz.openrdf.sail.allegrographserver import AllegroGraphServer
from franz.openrdf.sail.spec import reason

from oteapi.models import AttrDict, TripleStoreConfig
from oteapi.models.mappingconfig import RDFTriple

if TYPE_CHECKING:  # pragma: no cover
    from typing import Any, Dict, Union


class TripleStore:
    """
    This class is available to import from `oteapi.triplestore`, e.g.:

    ```python
    from oteapi.triplestore import TripleStore
    ```
    Init must initialize the triple store connection

    Args:
        config (Union[TripleStoreConfig, Dict[str, Any]]): RDF triple-store
            configuration.

    Attributes:
        config (TripleStoreConfig): The RDF triple-store configuration.

    """

    def __init__(
        self,
        config: "Union[TripleStoreConfig, Dict[str, Any]]",
    ) -> None:
        if isinstance(config, (dict, AttrDict)):
            self.config = TripleStoreConfig(**config)
        elif isinstance(config, TripleStoreConfig):
            self.config = config
        else:
            raise TypeError(
                "config should be either a `TripleStoreConfig` data model or a "
                "dictionary."
            )
        self.server = AllegroGraphServer(
            self.config.agraphHost,
            self.config.agraphPort,
            self.config.user.get_secret_value(),  # type: ignore [union-attr]
            self.config.password.get_secret_value(),  # type: ignore [union-attr]
        )

    def add(self, triples: RDFTriple) -> None:
        """
        Add triples to the triplestore.

        Args:
            triples: triples turtle format(<s> <o> <p>.).

        """
        with ag_connect(
            self.config.repositoryName,
            host=self.config.agraphHost,
            port=self.config.agraphPort,
            user=self.config.user.get_secret_value(),  # type: ignore [union-attr]
            password=self.config.password.get_secret_value(),  # type: ignore [union-attr]  # pylint: disable=line-too-long
        ) as connection:
            connection.addData(triples)
            connection.close()

    def get(self, sparql_query: str) -> "Any":
        """Return the query result.

        Args:
            sparql_query: The SPARQL search query.

        Returns:
            The output of the search query in the form of a list of RDF triples.

        """
        connection = self.server.openSession(
            reason("<" + str(self.config.repositoryName) + ">")
        )
        try:
            tuple_query = connection.prepareTupleQuery(query=sparql_query)
            response = []

            with tuple_query.evaluate(output_format=TupleFormat.JSON) as results:
                for result in results:
                    triple = {}
                    if "'s': " in str(result):
                        triple["s"] = str(result.getValue("s"))
                    if "'p': " in str(result):
                        triple["p"] = str(result.getValue("p"))
                    if "'o': " in str(result):
                        triple["o"] = str(result.getValue("o"))
                    response.append(triple)
            connection.close()
            return response
        except RequestError as error:
            return {"Error": error}

    def update_delete(self, sparql_query: str) -> None:
        """Remove and update triples.

        Useful for modifying and cleaning up mappings.

        Args:
            sparql_query: The sparql update/delete query.
        Returns:
            True if update was successful.

        """
        with ag_connect(
            self.config.repositoryName,
            host=self.config.agraphHost,
            port=self.config.agraphPort,
            user=self.config.user.get_secret_value(),  # type: ignore [union-attr]
            password=self.config.password.get_secret_value(),  # type: ignore [union-attr]  # pylint: disable=line-too-long
        ) as connection:
            update_query = connection.prepareUpdate(query=sparql_query)
            update_query.evaluate()
            connection.close()

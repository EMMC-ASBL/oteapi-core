"""
Triplestore using Allegrograph
https://franz.com/agraph/support/documentation/current/python/api.html
https://franz.com/agraph/support/documentation/current/agraph-introduction.html

Features:

- Store mapping data (triple format)
- AllegroGraph has a well documented python API package


"""
# pylint: disable=too-many-arguments

import json
from typing import TYPE_CHECKING
from franz.openrdf.sail.allegrographserver import AllegroGraphServer  # type: ignore
from franz.openrdf.sail.spec import reason  # type: ignore
from franz.openrdf.rio.tupleformat import TupleFormat
from franz.openrdf.connect import ag_connect
from oteapi.models import AttrDict, TripleStoreConfig

if TYPE_CHECKING:  # pragma: no cover
    from typing import Any, Dict, Union


class TripleStore:
    """
    This class is available to import from `oteapi.triplestore`, e.g.:

    ```python
    from oteapi.triplestore import TripleStore
    ```
    Init must initialize the triple store connection?

    Args:
        config (Union[TripleStoreConfig, Dict[str, Any]]): Download configurations.

    Attributes:
        config: TripleStoreConfig instance.

    """

    def __init__(
        self,
        config: "Union[TripleStoreConfig, Dict[str, Any]]",
    ) -> None:
        if config is None:
            self.config = TripleStoreConfig()
        elif isinstance(config, (dict, AttrDict)):
            self.config = TripleStoreConfig(**config)
        elif isinstance(config, TripleStoreConfig):
            self.config = config
        else:
            raise TypeError(
                "config should be either a `TripleStoreConfig` data model or a "
                "dictionary."
            )
        self.server = AllegroGraphServer(self.config.agraphHost,
                                         self.config.agraphPort,
                                         self.config.agraphUser,
                                         self.config.agraphPassword)

    def add(
        self,
        triples: "Any"
    ) -> str:
        """
        Add triples to the triplestore.

        Args:
            triples: triples turtle format(<s> <o> <p>.).           

        """
        connection = ag_connect(self.config.repositoryName,
                                host=self.config.agraphHost,
                                port=self.config.agraphPort,
                                user=self.config.agraphUser,
                                password=self.config.agraphPassword)
        connection.addData(triples)
        connection.close()
        return "Triples successfully added"

    def get(self, sparqlQuery: str) -> "Any":
        """Return the query result.

        Args:
            sparqlQuery: The SPARQL search query.

        Returns:
            The output of the search query in the form of subject, object and predicate.

        """
        connection = self.server.openSession(
            reason("<" + str(self.config.repositoryName) + ">"))
        TupleQuery = connection.prepareTupleQuery(query=sparqlQuery)
        response = []
        results = TupleQuery.evaluate(output_format=TupleFormat.JSON)
        with TupleQuery.evaluate(output_format=TupleFormat.JSON) as results:
            for result in results:
                tripleSet = {}
                if ("'s': " in str(result)):
                    tripleSet['s'] = str(result.getValue("s"))
                if ("'p': " in str(result)):
                    tripleSet['p'] = str(result.getValue("p"))
                if ("'o': " in str(result)):
                    tripleSet['o'] = str(result.getValue("o"))
                response.append((tripleSet))
        connection.close()
        return json.dumps(response)

    def updateDelete(self, sparqlQuery: str) -> None:
        """Remove and update triples.

        Useful for modifying and cleaning up mappings.

        Args:
            sparqlQuery: The sparql update/delete query.
        Returns:
            True if update was successful.

        """
        connection = ag_connect(self.config.repositoryName,
                                host=self.config.agraphHost,
                                port=self.config.agraphPort,
                                user=self.config.agraphUser,
                                password=self.config.agraphPassword)
        updateQuery = connection.prepareUpdate(query=sparqlQuery)
        response = updateQuery.evaluate()
        connection.close()
        return response

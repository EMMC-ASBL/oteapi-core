"""Utility functions for representing instances of pydantic models as rdf.

This module uses JSON-LD with a shared context on https://w3id.org/domain/oteio/context
"""

import io
import json
from pathlib import Path
from typing import TYPE_CHECKING

import rdflib
import yaml

if TYPE_CHECKING:  # pragma: no cover
    from typing import Any, Optional, TextIO, Union

    # import tripper


def load_content(
    source: "Optional[Union[Path, str, TextIO]]" = None,
    data: "Optional[str]" = None,
    format: "Optional[str]" = None,
) -> "Any":
    """Load content from yaml or json source.

    Arguments:
        source: File name or file-like object with data documentation to add.
        data: String containing the data documentation to add.
        format: Input format. One of: "yaml", "json".
            By default it will be inferred from `source` or `data`.

    Returns:
        Python representation of the content.
    """
    if not source and not data:
        raise TypeError("Either `source` or `data` must be given.")

    if source and isinstance(source, (str, Path)):
        with open(source, "rt") as f:
            return load_content(source=f, format=format)

    if format is None:
        if source:
            format = Path(source.name).suffix
        elif data.lstrip().startswith("---"):
            format = "yaml"
        elif data.lstrip().startswith("{"):
            format = "json"

    if format is None:
        raise ValueError("Format cannot be inferred.  Use `format` argument.")

    format = format.lstrip(".").lower()
    if format in ("yaml", "yml"):
        if not source:
            source = io.StringIO(data)
        content = yaml.safe_load(source)
    elif format in ("json"):
        content = json.load(source) if source else json.loads(data)
    else:
        raise TypeError(f"Unsupported format: {format}")

    return content


def add_resource(
    source: "Optional[Union[Path, str, TextIO]]" = None,
    data: "Optional[dict, str]" = None,
    format: "Optional[str]" = None,
    graph: "Optional[Union[rdflib.Graph, Any]]" = None,
) -> "Union[rdflib.Graph, Any]":
    """Add documentation of data resource(s) to triplestore.

    Arguments:

        source: File name or file-like object with data documentation
            to add.
        data: Dict or string containing the data documentation to add.
        format: Input format. One of: "yaml", "json".
            By default it will be inferred from `source` or `data`.
        graph: The graph to add the documentation to.  It can be a
            rdflib.Graph object or any type that has a parse() method
            that supports json-ld.
            If not given, a new rdflib.Graph object will be created.

    Returns:
        The provided graph or a new rdflib.Graph object, if `graph` is
        None.
    """
    if isinstance(data, dict):
        content = data.copy()
    else:
        content = load_content(source=source, data=data, format=format)

    if not isinstance(content, dict):
        raise TypeError("Expected input content to be a dict.")

    if "@context" not in content:
        content["@context"] = "https://w3id.org/emmo/domain/oteio/context"

    if not graph:
        graph = rdflib.Graph()

    with open("xxx.json", "wt") as f:
        json.dump(content, f, indent=2)

    # print("=====================================")
    # print(json.dumps(content, indent=2))

    # graph.parse(data=content, format="json-ld")
    graph.parse(source="xxx.json", format="json-ld")
    return graph

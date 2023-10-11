"""Utility functions for handling paths."""
import warnings
from pathlib import Path, PureWindowsPath
from typing import TYPE_CHECKING
from urllib.parse import ParseResult, urlparse

if TYPE_CHECKING:  # pragma: no cover
    from typing import Union

    from pydantic import AnyUrl


def uri_to_path(uri: "Union[str, AnyUrl, ParseResult]") -> Path:
    """Convert URI to pathlib.Path.

    Support both Windows and Posix path types.

    Information:
        `urllib.parse.urlparse()` leaves an initial slash in front of the drive letter
        when parsing a file URL for an absolute path on Windows.

        Example: `urlparse("file:///C:/Windows").path` -> `"/C:/Windows"`

        To solve this, the initial forward slash is removed prior to casting to
        `pathlib.Path`.

    Parameters:
        uri: The URI/IRI/URL. Either as a string or a parsed URL.

    Returns:
        A properly converted URI/IRI/URL to `pathlib.Path`.

    """
    if not isinstance(uri, ParseResult):
        uri = urlparse(str(uri))

    uri_path = (uri.netloc + uri.path) if uri.scheme == "file" else uri.path

    if uri.scheme != "file":
        warnings.warn(
            "A 'file'-scheme was expected for the 'uri' in 'uri_to_path()', instead a "
            f"{uri.scheme!r} was received. Still converting to `pathlib.Path` using "
            "the 'path' of the URI."
        )

    path = Path(uri_path)
    if isinstance(path, PureWindowsPath):
        path = Path(uri_path.lstrip("/"))
    return path

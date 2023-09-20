"""Import from pydantic through this module.

This is to ensure compatibility with pydantic v1 and v2.
"""


def get_pydantic_major_version() -> int:
    """Get the major version of pydantic.

    Returns:
        int: The major version of pydantic.
    """
    import pydantic

    return int(pydantic.VERSION.split(".", maxsplit=1)[0])


PYDANTIC_VERSION = get_pydantic_major_version()

if PYDANTIC_VERSION == 1:
    from pydantic import *
    from pydantic.fields import Undefined
elif PYDANTIC_VERSION == 2:
    from pydantic.v1 import *
    from pydantic.v1.fields import Undefined
else:
    raise NotImplementedError("Support for pydantic version >=3 is not implemented.")

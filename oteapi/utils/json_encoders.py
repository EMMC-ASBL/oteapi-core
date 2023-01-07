from typing import TYPE_CHECKING
import os
from distutils.util import strtobool


if TYPE_CHECKING:  # pragma: no cover
    from typing import Any, Dict, Union
    from pydantic import SecretStr


def encode_secrets(secret: "SecretStr") -> "Any":
    """Function for encording secrets when serialized to json"""
    if secret:
        return secret.get_secret_value()
    else:
        return secret

"""AttrDict for specifying user credentials or secrets."""
import json
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, Field, SecretStr

from oteapi.settings import settings

if TYPE_CHECKING:  # pragma: no cover
    from typing import Any, Callable


def json_dumps(model: dict, default: "Callable[[Any], Any]") -> "str":
    """Alternative function for dumping exposed
    secrets to json when model is serialized.

    Parameters:
        model: The pydantic model to serialize.
        default: A pass-through to the standard `json.dumps()`'s `default` parameter.
            From the `json.dumps()` doc-string: `default(obj)` is a function that should
            return a serializable version of `obj` or raise `TypeError`.
            The default simply raises `TypeError`.

    Returns:
        The result of `json.dumps()` after handling possible secrets.

    """
    return json.dumps(
        {
            key: (
                value.get_secret_value()
                if settings.expose_secrets and isinstance(value, SecretStr)
                else value
            )
            for key, value in model.items()
        },
        default=default,
    )


class SecretConfig(BaseModel, json_dumps=json_dumps):
    """Simple model for handling secret in other config-models."""

    user: Optional[SecretStr] = Field(None, description="User name for authentication.")
    password: Optional[SecretStr] = Field(
        None, description="Password for authentication."
    )
    token: Optional[SecretStr] = Field(
        None,
        description=(
            "An access token for providing access and meta data to an application."
        ),
    )
    client_id: Optional[SecretStr] = Field(
        None, description="Client ID for an OAUTH2 client."
    )
    client_secret: Optional[SecretStr] = Field(
        None, description="Client secret for an OAUTH2 client."
    )

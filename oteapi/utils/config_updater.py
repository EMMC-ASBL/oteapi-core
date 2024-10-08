"""Utility functions for updating GenericConfig instances."""

from __future__ import annotations

from typing import TYPE_CHECKING

from oteapi.models.genericconfig import GenericConfig

if TYPE_CHECKING:
    from typing import Any


def populate_config_from_session(
    session: dict[str, Any],
    config: GenericConfig,
) -> None:
    """
    Update the configuration attributes of a GenericConfig object
    using values from a session. If a key already exists in the
    config's configuration and has a different value from the session,
    an exception will be raised.

    Args:
        session (Dict): A session containing configuration attributes.
        config (GenericConfig): A GenericConfig object to be updated.
    """
    # Determine which keys to update
    keys_to_update = list(session.keys())

    for key in keys_to_update:
        if (
            # "configuration" in config
            key in config.configuration
            and session[key] != config.configuration[key]
        ):
            raise ValueError(
                f"Key '{key}' in config has different value than in session."
            )

        try:
            config.configuration[key] = session[key]
        except Exception as error:
            raise RuntimeError(
                f"Failed to update key '{key}' in the config. Reason: {error!s}"
            ) from error

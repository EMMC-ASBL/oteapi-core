"""Plugin loader."""
import importlib
from importlib.metadata import entry_points
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from types import ModuleType
    from typing import List, Set


class PluginInterface:
    """Call the plugin to be initialized."""

    @staticmethod
    def initialize() -> None:
        """Initialize the plugin."""


def import_module(name: str) -> "ModuleType":
    """Import module.

    Parameters:
        name: The module to import. Must be a proper importable python module path,
            e.g., `"oteapi.plugins.plugins"`.

    Returns:
        The imported module.

    """
    return importlib.import_module(name)


def get_all_entry_points() -> "List[str]":
    """Retrieve all importable OTE-API entry points.

    Returns:
        An alphabetically sorted list of module paths for importable OTE-API
        strategies in OTE-API plugins.

    """
    plugin_strategies: "Set[str]" = set()
    for group, entry_point in entry_points().items():
        if group.startswith("oteapi."):
            plugin_strategies |= set(_.module for _ in entry_point)
    return sorted(plugin_strategies)


def load_plugins() -> None:
    """Load plugins from the environment's entry points."""
    for plugin_name in get_all_entry_points():
        import_module(plugin_name)

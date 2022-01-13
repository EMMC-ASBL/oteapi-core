"""Plugin loader."""
import importlib
from importlib.metadata import entry_points
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import List, Set


class PluginInterface:  # pylint: disable=R0903
    """Call the plugin to be initialized"""

    @staticmethod
    def initialize() -> None:
        """Initialize the plugin"""


def import_module(name: str) -> PluginInterface:
    """import modules"""
    return importlib.import_module(name)  # type: ignore


def get_all_entry_points() -> "List[str]":
    """Retrieve all importable oteapi entry points."""
    plugin_strategies: "Set[str]" = set()
    for group, entry_point in entry_points().items():
        if group.startswith("oteapi."):
            plugin_strategies |= set(_.module for _ in entry_point)
    return sorted(plugin_strategies)


def load_plugins() -> None:
    """Load plugins from the plugins list"""
    for plugin_name in get_all_entry_points():
        import_module(plugin_name)

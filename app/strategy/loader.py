"""Plugin loader."""
import importlib
from typing import List


class PluginInterface:  # pylint: disable=R0903
    """Call the plugin to be initialized"""

    @staticmethod
    def initialize() -> None:
        """Initialize the plugin"""


def import_module(name: str) -> PluginInterface:
    """import modules"""
    return importlib.import_module(name)  # type: ignore


def load_plugins(plugins: List[str]) -> None:
    """Load plugins from the plugins list"""
    for plugin_name in plugins:
        import_module(plugin_name)

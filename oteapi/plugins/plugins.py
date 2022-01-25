"""Plugin loader."""
import importlib
import re
from collections import abc
from enum import Enum
from functools import lru_cache
from importlib.metadata import entry_points
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from importlib.metadata import EntryPoint
    from types import ModuleType
    from typing import Dict, Iterable, Iterator, Optional, Set, Tuple, Union


class EntryPointStrategy:
    """A strategy realized from an entry point.

    Raises:
        ValueError: If the entry point name is not properly defined.

    """

    ENTRY_POINT_NAME_REGEX = re.compile(
        r"^(?P<package_name>[a-z_]+)" r"\.(?P<strategy_name>[a-z._]+)$"
    )
    ENTRY_POINT_NAME_SEPARATOR = ":"

    def __init__(self, entry_point: "EntryPoint") -> None:
        self._entry_point = entry_point
        self._match = self.ENTRY_POINT_NAME_REGEX.match(self._entry_point.name)

        if self._match is None:
            raise ValueError(
                "Could not determine package name and/or strategy name for entry "
                f"point: {self.full_name}"
            )

    @lru_cache
    @property
    def type(self) -> str:
        """The strategy type.

        One part of the (strategy type, strategy name)-tuple.
        """
        return self._entry_point.group[len("oteapi.") :]

    @lru_cache
    @property
    def name(self) -> str:
        """The strategy name.

        One part of the (strategy type, strategy name)-tuple.
        """
        return self._match.group("strategy_name").replace(".", "/")

    @lru_cache
    @property
    def strategy(self) -> Tuple[str, str]:
        """The unique index identifier for the strategy."""
        return self.type, self.name

    @lru_cache
    @property
    def package(self) -> str:
        """The importable base package name for the strategy plugin."""
        return self._match.group("package_name")

    @lru_cache
    @property
    def module(self) -> str:
        """The fully resolved importable module path."""
        return self._entry_point.module

    @lru_cache
    @property
    def full_name(self) -> str:
        """The full entry point name."""
        return f"{self._entry_point.group}{self.ENTRY_POINT_NAME_SEPARATOR}{self._entry_point.name}"


class EntryPointStrategyCollection(abc.Collection):
    """A collection of
    [`EntryPointStrategy`][oteapi.plugins.plugins.EntryPointStrategy]s."""

    def __init__(
        self, entry_points: "Optional[Iterable[EntryPointStrategy]]" = None
    ) -> None:
        self._entry_points: "Set[EntryPointStrategy]" = (
            set(entry_points) if entry_points else set()
        )

    def add(self, *entry_points: EntryPointStrategy) -> None:
        """Add entry points to the collection."""
        self._entry_points |= set(entry_points)

    def __len__(self) -> int:
        """Total number of entry points in the collection."""
        return len(self._entry_points)

    def __contains__(self, item: "Union[EntryPointStrategy, str]") -> bool:
        """Whether or not `item` is contained in the collection.

        One can test with an `EntryPointStrategy` or a string of an entry point
        strategy's name or full name.
        """
        if isinstance(item, EntryPointStrategy):
            return item in self._entry_points
        if isinstance(item, str):
            for entry_point in self._entry_points:
                if entry_point.name == item or entry_point.full_name == item:
                    return True
            return False
        return False

    def __iter__(self) -> "Iterator[EntryPointStrategy]":
        """Return an iterator for the contained entry points."""
        yield from self._entry_points


class OteapiEntryPointGroup(Enum):
    """A valid OTE-API entry point group."""

    DOWNLOAD = "scheme"
    FILTER = "filterType"
    MAPPING = "mappingType"
    PARSE = "mediaType"
    RESOURCE = "accessService"
    TRANSFORMATION = "transformation_type"

    @classmethod
    def all_values(cls) -> Tuple[str]:
        """Return all enumeration values."""
        return tuple(_.value for _ in cls)


def import_module(name: str) -> "ModuleType":
    """Import module.

    Parameters:
        name: The module to import. Must be a proper importable python module path,
            e.g., `"oteapi.plugins.plugins"`.

    Returns:
        The imported module.

    """
    return importlib.import_module(name)


def get_all_entry_points() -> "Dict[OteapiEntryPointGroup, Tuple[EntryPointStrategy]]":
    """Retrieve all importable OTE-API entry points.

    Returns:
        An alphabetically sorted list of module paths for importable OTE-API
        strategies in OTE-API plugins.

    """
    plugin_strategies: "Dict[OteapiEntryPointGroup,  Tuple[EntryPointStrategy]]" = {}

    for group, oteapi_entry_points in entry_points().items():
        if (
            group.startswith("oteapi.")
            and group[len("oteapi.") :] in OteapiEntryPointGroup.all_values()
        ):
            strategy_type = OteapiEntryPointGroup(group[len("oteapi.") :])
            plugin_strategies[strategy_type] = tuple(
                set(EntryPointStrategy(_) for _ in oteapi_entry_points)
            )
    return plugin_strategies


def load_plugins() -> None:
    """Load plugins from the environment's entry points."""
    for plugin_name in get_all_entry_points():
        import_module(plugin_name)

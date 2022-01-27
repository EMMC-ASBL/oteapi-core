"""Plugin loader."""
import importlib
import re
from collections import abc
from enum import Enum
from importlib.metadata import entry_points as get_entry_points
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from importlib.metadata import EntryPoint
    from typing import Any, Iterable, Iterator, Optional, Set, Tuple, Type, Union

    from oteapi.interfaces import IStrategy


class EntryPointNotFound(Exception):
    """A given strategy implementation (class) cannot be found from the given entry
    point value."""


class OteapiStrategyType(Enum):
    """A valid OTE-API entry point group."""

    DOWNLOAD = "scheme"
    FILTER = "filterType"
    MAPPING = "mappingType"
    PARSE = "mediaType"
    RESOURCE = "accessService"
    TRANSFORMATION = "transformation_type"

    @classmethod
    def all_values(cls) -> "Tuple[str, ...]":
        """Return all enumeration values."""
        return tuple(_.value for _ in cls)


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

        match = self.ENTRY_POINT_NAME_REGEX.match(self._entry_point.name)
        if match is None:
            raise ValueError(
                "Could not determine package name and/or strategy name for entry "
                f"point: {self.full_name}"
            )

        self._match = match
        self._type = OteapiStrategyType(self._entry_point.group[len("oteapi.") :])
        self._implementation: "Optional[Type[IStrategy]]" = None

    @property
    def type(self) -> OteapiStrategyType:
        """The strategy type.

        One part of the (strategy type, strategy name)-tuple.
        """
        return self._type

    @property
    def name(self) -> str:
        """The strategy name.

        One part of the (strategy type, strategy name)-tuple.

        Note:
            Single periods (`.`) in the entry point name will become forward slashes
            (`/`). And double periods (`..`) will become single periods (`.`).

            Conversions:

            - `.` -> `/`
            - `..` -> `.`

            Example:
                ```ini
                oteapi.mediaType =
                  oteapi.application.vnd..sqlite3 = ...
                ```

                Defines the *parse* strategy name: `application/vnd.sqlite`
                From the `oteapi` package.

        Note:
            **For developers**.

            The order of the `replace()` methods is important.

            By first replacing all periods (`.`) with forward slashes (`/`) we can be
            sure all double forward slashes (`//`) have come from double periods (`..`)
            because a forward slash is not a valid character in the entry point name.

        """
        return self._match.group("strategy_name").replace(".", "/").replace("//", ".")

    @property
    def strategy(self) -> "Tuple[OteapiStrategyType, str]":
        """The unique index identifier for the strategy."""
        return self.type, self.name

    @property
    def package(self) -> str:
        """The importable base package name for the strategy plugin."""
        return self._match.group("package_name")

    @property
    def module(self) -> str:
        """The fully resolved importable module path."""
        return self._entry_point.module  # type: ignore[attr-defined]

    @property
    def full_name(self) -> str:
        """The full entry point name."""
        return f"{self._entry_point.group}{self.ENTRY_POINT_NAME_SEPARATOR}{self._entry_point.name}"

    def __str__(self) -> str:
        """String representation for EntryPointStrategy."""
        return self.full_name

    @property
    def implementation_name(self) -> str:
        """The EntryPoint attr, which should be the strategy implementation class
        name."""
        return self._entry_point.attr  # type: ignore[attr-defined]

    @property
    def implementation(self) -> "Type[IStrategy]":
        """The actual strategy implementation."""
        if self._implementation is None:
            self._implementation = self._load_implementation()
        return self._implementation

    def _load_implementation(self) -> "Type[IStrategy]":
        """Load the strategy implementation.

        Because the actual importing of the module does not happen until this method is
        called, we are lazily loading in the strategy implementation.

        There is no need to check through the `globals()` built-in for whether the
        module and class have already been imported, because this caching layer is
        already implemented in the `importlib` API.

        Raises:
            oteapi.plugins.plugins.EntryPointNotFound: If the strategy implementation
                (class) the entry point is pointing to cannot be found in the module or
                if the module cannot be imported.

        Returns:
            The imported strategy implementation (class).

        """
        try:
            module = importlib.import_module(self.module)
        except ImportError as exc:
            raise EntryPointNotFound(
                f"{self.module} cannot be imported. Did you install the "
                f"{self.package!r} package?"
            ) from exc

        if hasattr(module, self.implementation_name):
            return getattr(module, self.implementation_name)
        raise EntryPointNotFound(
            f"{self.implementation_name} cannot be found in {self.module}"
        )


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

    def remove(self, *entry_points: EntryPointStrategy) -> None:
        """Remove entry points from the collection."""
        self._entry_points -= set(entry_points)

    def exclusive_add(self, *entry_points: EntryPointStrategy) -> None:
        """Exclusively add entry points to the collection.

        Raises:
            KeyError: If an entry point to be added already exists in the collection.

        """
        for entry_point in entry_points:
            if entry_point in self:
                raise KeyError(f"{entry_point} already exists in {self}.")
            self.add(entry_point)

    def __len__(self) -> int:
        """Total number of entry points in the collection."""
        return len(self._entry_points)

    def __contains__(self, item: "Any") -> bool:
        """Whether or not `item` is contained in the collection.

        One can test with an `EntryPointStrategy` or a string of an entry point
        strategy's name or full name.
        """
        if isinstance(item, EntryPointStrategy):
            return item in self._entry_points
        if isinstance(item, str):
            for entry_point in self._entry_points:
                if item in (entry_point.name, entry_point.full_name):
                    return True
            return False
        # For any other type:
        return False

    def __iter__(self) -> "Iterator[EntryPointStrategy]":
        """Return an iterator for the contained entry points."""
        yield from self._entry_points

    def __getitem__(self, key: "Any") -> EntryPointStrategy:
        """Return an entry point item in the collection.

        Raises:
            KeyError: If an entry point cannot be found in the collection.

        Returns:
            An entry point in the collection representing the key.

        """
        return self.get_entry_point(key)

    def get_entry_point(
        self, key: "Union[EntryPointStrategy, str]"
    ) -> EntryPointStrategy:
        """Retrieve an entry point from the collection.

        Raises:
            KeyError: If an entry point cannot be found in the collection.

        Returns:
            An entry point in the collection representing the key.

        """
        if isinstance(key, (EntryPointStrategy, str)):
            if key not in self:
                raise KeyError(f"{key} not found in {self}")
            return self._get_entry_point(key)
        raise TypeError("key should either of type EntryPointStrategy or a string.")

    def _get_entry_point(
        self, key: "Union[EntryPointStrategy, str]"
    ) -> EntryPointStrategy:
        """Helper method for retrieving an entry point from the collection.

        Important:
            It is expected that the entry point representing the key exists in the
            collection. For example through a `key in self` test.

        Raises:
            RuntimeError: If an entry point cannot be found in the collection, since
                this is a requirement.

        Returns:
            An entry point in the collection representing the key.

        """
        if isinstance(key, EntryPointStrategy):
            return key
        if isinstance(key, str):
            for entry_point in self._entry_points:
                if key in (entry_point.name, entry_point.full_name):
                    return entry_point
        raise RuntimeError(
            f"{key} not found in {self}, which is a requirement for the "
            "_get_entry_point method."
        )


def get_strategy_entry_points(
    strategy_type: "Union[OteapiStrategyType, str]",
) -> EntryPointStrategyCollection:
    """Retrieve all entry points from a specific strategy type.

    Raises:
        ValueError: If the strategy type is not supported.

    Returns:
        A collection of entry points for the specific strategy type.

    """
    try:
        strategy_type = OteapiStrategyType(strategy_type)
    except ValueError as exc:
        raise ValueError(
            "Strategy type "
            f"{strategy_type if isinstance(strategy_type, str) else str(strategy_type.value)!r}"
            " is not supported."
        ) from exc

    collection = EntryPointStrategyCollection()
    for group, oteapi_entry_points in get_entry_points().items():
        if group.startswith("oteapi.") and group[len("oteapi.") :] == str(
            strategy_type.value
        ):
            collection.add(*(EntryPointStrategy(_) for _ in oteapi_entry_points))
    return collection

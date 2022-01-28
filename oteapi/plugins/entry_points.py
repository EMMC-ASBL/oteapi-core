"""Load plugins through entry points.

This module deals with handling all plugged in strategies through the entry points API
and importlib metadata API.

Special functionality is put in place to handle the OTE-API-specific entry points.

Since the entry points are information complete in and of themselves, there is no need
to import actual strategy classes until they are truly needed.
This therefore implements lazy loading of all plugin strategies.
"""
import importlib
import re
from collections import abc
from enum import Enum
from functools import lru_cache
from importlib.metadata import entry_points as get_entry_points
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from importlib.metadata import EntryPoint
    from typing import Any, Iterable, Iterator, Optional, Set, Tuple, Type, Union

    from oteapi.interfaces import IStrategy


class EntryPointNotFound(Exception):
    """A given strategy implementation (class) cannot be found from the given entry
    point value."""


class StrategyType(Enum):
    """An enumeration of available strategy types.

    Available strategy types:

    - download
    - filter
    - mapping
    - parse
    - resource
    - transformation

    """

    DOWNLOAD = "download"
    FILTER = "filter"
    MAPPING = "mapping"
    PARSE = "parse"
    RESOURCE = "resource"
    TRANSFORMATION = "transformation"

    @lru_cache
    def map_to_field(self) -> str:
        """Map enumeration value to the strategy type's field."""
        return {
            "download": "scheme",
            "filter": "filterType",
            "mapping": "mappingType",
            "parse": "mediaType",
            "resource": "accessService",
            "transformation": "transformation_type",
        }[self.value]

    @classmethod
    @lru_cache
    def map_from_field(cls, strategy_type_field: str) -> "StrategyType":
        """Map the strategy type's field to enumeration.

        Parameters:
            strategy_type_field: The strategy type's field. E.g., `scheme` for
                `download`.

        Raises:
            KeyError: If the `strategy_type_field` is not valid.

        Returns:
            An enumeration instance representing the strategy type's field.

        """
        return {
            "scheme": cls.DOWNLOAD,
            "filterType": cls.FILTER,
            "mappingType": cls.MAPPING,
            "mediaType": cls.PARSE,
            "accessService": cls.RESOURCE,
            "transformation_type": cls.TRANSFORMATION,
        }[strategy_type_field]

    @classmethod
    @lru_cache
    def init(cls, value: str) -> "StrategyType":
        """Initialize a StrategyType with more than just the enumeration value.

        This method allows one to also initialize a StrategyType with an actual
        strategy type string, e.g., `scheme`, `mediaType`, etc.

        Raises:
            ValueError: As normal if the enumeration value is not valid.

        """
        try:
            return cls.map_from_field(value)
        except KeyError:
            return cls(value)

    @classmethod
    @lru_cache
    def all_values(cls) -> "Tuple[str, ...]":
        """Return all values."""
        return tuple(_.value for _ in cls)


class EntryPointStrategy:
    """A strategy realized from an entry point.

    An entry point strategy is made unique by its "strategy", i.e., its
    (strategy type, strategy name)-tuple, e.g., `("download", "https")`.
    This tuple can be retrieved from the
    [`strategy`][oteapi.plugins.entry_points.EntryPointsStrategy.strategy] property,
    where the strategy type is represented by the
    [`StrategyType`][oteapi.plugins.entry_points.StrategyType] enumeration.

    Note:
        It may be that in the future an entry points strategy is made unique by
        its "full name" instead, i.e., the entry point group + the entry points name,
        e.g., `oteapi.download:oteapi.https`.
        This value can be retrieved from the
        [`full_name`][oteapi.plugins.entry_points.EntryPointStrategy.full_name]
        property.

        This is a condition for uniqueness that is considered to be a superset of the
        current condition for uniqueness.
        It adds an extra package-specific uniqueness trait, allowing for different
        packages to implement the same strategies (which is currently not allowed
        according to the condition of uniqueness explained above).

        Currently there is no consensus on the API for handling this added strategy
        ambiguity.

    Raises:
        ValueError: If the entry point name is not properly defined.

    """

    ENTRY_POINT_NAME_REGEX = re.compile(
        r"^(?P<package_name>[a-z_]+)\.(?P<strategy_name>.+)$"
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
        self._type = StrategyType(self._entry_point.group[len("oteapi.") :])
        self._implementation: "Optional[Type[IStrategy]]" = None

    @property
    def type(self) -> StrategyType:
        """The strategy type.

        One part of the (strategy type, strategy name)-tuple.
        """
        return self._type

    @property
    def name(self) -> str:
        """The strategy name.

        One part of the (strategy type, strategy name)-tuple.
        """
        return self._match.group("strategy_name")

    @property
    def strategy(self) -> "Tuple[StrategyType, str]":
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
        return self.full_name

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(entry_point={self._entry_point!r})"

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
            EntryPointNotFound: If the strategy implementation (class) the entry point
                is pointing to cannot be found in the module or if the module cannot be
                imported.

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

    def __eq__(self, other: "Any") -> bool:
        if isinstance(other, self.__class__):
            return hash(self) == hash(other)
        return False

    def __hash__(self) -> int:
        return hash(self.strategy)


class EntryPointStrategyCollection(abc.Collection):
    """A collection of
    [`EntryPointStrategy`][oteapi.plugins.entry_points.EntryPointStrategy]s."""

    def __init__(
        self, entry_points: "Optional[Iterable[EntryPointStrategy]]" = None
    ) -> None:
        self._entry_points: "Set[EntryPointStrategy]" = (
            set(entry_points) if entry_points else set()
        )

    def add(self, *entry_points: EntryPointStrategy) -> None:
        """Add entry points to the collection.

        Parameters:
            entry_points: Entry points to add to the collection.

        """
        self._entry_points |= set(entry_points)

    def remove(self, *entry_points: EntryPointStrategy) -> None:
        """Remove entry points from the collection.

        Parameters:
            entry_points: Entry points to remove from the collection.

        """
        self._entry_points -= set(entry_points)

    def exclusive_add(self, *entry_points: EntryPointStrategy) -> None:
        """Exclusively add entry points to the collection.

        Parameters:
            entry_points: Entry points to add to the collection.

        Raises:
            KeyError: If an entry point to be added already exists in the collection.

        """
        for entry_point in entry_points:
            if entry_point in self:
                raise KeyError(f"{entry_point} already exists in {self}.")
            self.add(entry_point)

    def __len__(self) -> int:
        return len(self._entry_points)

    def __contains__(self, item: "Any") -> bool:
        """Whether or not `item` is contained in the collection.

        One can test with an `EntryPointStrategy` or a string of an entry point
        strategy's name or full name.

        Parameters:
            item: Item to test whether it is contained in the collection.

        Returns:
            Whether or not `item` is contained in the collection.
            If the `item` is an unrecognized type, `False` will be returned.

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
        yield from self._entry_points

    def __getitem__(self, key: "Any") -> EntryPointStrategy:
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

    def __eq__(self, other: "Any") -> bool:
        if isinstance(other, self.__class__):
            return hash(self) == hash(other)
        return False

    def __hash__(self) -> int:
        return hash(self._entry_points)

    def __str__(self) -> str:
        return (
            f"<{self.__class__.__name__}: Length={len(self)} "
            f"Strategy type(s)={','.join(_.type.value for _ in self._entry_points)}>"
        )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(entry_points=*{self._entry_points!r})"


def get_strategy_entry_points(
    strategy_type: "Union[StrategyType, str]",
    enforce_uniqueness: bool = True,
) -> EntryPointStrategyCollection:
    """Retrieve all entry points from a specific strategy type.

    Raises:
        ValueError: If the strategy type is not supported.
        KeyError: If `enforce_uniqueness` is `True` and an entry point strategy is
            duplicated.

    Parameters:
        strategy_type: A strategy type for which the entry points will be retrieved.
        enforce_uniqueness: Whether or not duplicate entry point strategies are
            allowed. Defaults to `True`, meaning duplicates are *not* allowed.

    Returns:
        A collection of entry points for the specific strategy type.

    """
    try:
        strategy_type = StrategyType(strategy_type)
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
            if enforce_uniqueness:
                collection.exclusive_add(
                    *(EntryPointStrategy(_) for _ in oteapi_entry_points)
                )
            else:
                collection.add(*(EntryPointStrategy(_) for _ in oteapi_entry_points))
    return collection

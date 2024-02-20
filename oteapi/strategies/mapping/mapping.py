"""Mapping filter strategy."""

from typing import TYPE_CHECKING, Dict, List

from pydantic.dataclasses import Field, dataclass

from oteapi.models import AttrDict, MappingConfig, RDFTriple

if TYPE_CHECKING:  # pragma: no cover
    pass


class MappingAttrDict(AttrDict):
    """AttrDict model for mappings."""

    prefixes: Dict[str, str] = Field(
        ...,
        description=(
            "Dictionary of shortnames that expands to an IRI "
            "given as local value/IRI-expansion-pairs."
        ),
    )
    triples: List[RDFTriple] = Field(
        ...,
        description="List of semantic triples given as (subject, predicate, object).",
    )


@dataclass
class MappingStrategy:
    """Strategy for a mapping.

    The mapping strategy simply adds more prefixes and triples to the
    `prefixes` and `triples` fields in the session such that they are
    available for other strategies, like function strategies that convert
    between data models.

    Nothing is returned to avoid deleting existing mappings.

    **Registers strategies**:

    - `("mappingType", "triples")`

    """

    mapping_config: MappingConfig

    def initialize(self) -> MappingAttrDict:
        """Initialize strategy."""

        return MappingAttrDict(
            prefixes=self.mapping_config.prefixes, triples=self.mapping_config.triples
        )

    def get(self) -> AttrDict:
        """Execute strategy and return a dictionary."""
        return AttrDict()

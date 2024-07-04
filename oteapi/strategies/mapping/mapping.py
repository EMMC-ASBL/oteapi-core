"""Mapping filter strategy."""

from __future__ import annotations

from pydantic.dataclasses import Field, dataclass

from oteapi.models import AttrDict, MappingConfig, RDFTriple


class MappingStrategyConfig(AttrDict):
    """AttrDict model for mappings."""

    prefixes: dict[str, str] = Field(
        ...,
        description=(
            "Dictionary of shortnames that expands to an IRI "
            "given as local value/IRI-expansion-pairs."
        ),
    )
    triples: list[RDFTriple] = Field(
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

    def initialize(self) -> MappingStrategyConfig:
        """Initialize strategy."""

        return MappingStrategyConfig(
            prefixes=self.mapping_config.prefixes, triples=self.mapping_config.triples
        )

    def get(self) -> AttrDict:
        """Execute strategy and return a dictionary."""
        return AttrDict()

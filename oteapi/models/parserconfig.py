"""Pydantic Parser Configuration Data Model."""

from pydantic import AnyHttpUrl, Field

from oteapi.models.genericconfig import GenericConfig


class ParserConfig(GenericConfig):
    """Parser Strategy Data Configuration."""

    parserType: str = Field(
        ...,
        description="Type of registered parser strategy.",
        IRI="http://purl.org/dc/terms/type",
    )  # type: ignore
    entity: AnyHttpUrl = Field(
        ...,
        description="IRI to the metadata (entity) or collection of entities.",
        IRI="http://schema.org/URL",
    )  # type: ignore

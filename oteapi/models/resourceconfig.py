"""Pydantic Resource Configuration Data Model."""
# pylint: disable=line-too-long
from typing import TYPE_CHECKING, Optional

from pydantic import AnyUrl, Field, root_validator

from oteapi.models.genericconfig import GenericConfig
from oteapi.models.secretconfig import SecretConfig

if TYPE_CHECKING:  # pragma: no cover
    from typing import Any, Dict


class HostlessAnyUrl(AnyUrl):
    """AnyUrl, but allow not having a host."""

    host_required = False


class ResourceConfig(GenericConfig, SecretConfig):
    """Resource Strategy Data Configuration.

    Important:
        Either of the pairs of attributes `downloadUrl`/`mediaType` or
        `accessUrl`/`accessService` MUST be specified.

    """

    downloadUrl: Optional[HostlessAnyUrl] = Field(
        None,
        description=(
            "Definition: The URL of the downloadable file in a given format. E.g. CSV "
            "file or RDF file.\n\nUsage: `downloadURL` *SHOULD* be used for the URL at"
            " which this distribution is available directly, typically through a HTTPS"
            " GET request or SFTP."
        ),
    )
    mediaType: Optional[str] = Field(
        None,
        description=(
            "The media type of the distribution as defined by IANA "
            "[[IANA-MEDIA-TYPES](https://www.w3.org/TR/vocab-dcat-2/#bib-iana-media-types)]"
            ".\n\nUsage: This property *SHOULD* be used when the media"
            " type of the distribution is defined in IANA "
            "[[IANA-MEDIA-TYPES](https://www.w3.org/TR/vocab-dcat-2/#bib-iana-media-types)]."
        ),
    )
    accessUrl: Optional[HostlessAnyUrl] = Field(
        None,
        description=(
            "A URL of the resource that gives access to a distribution of "
            "the dataset. E.g. landing page, feed, SPARQL endpoint.\n\nUsage: "
            "`accessURL` *SHOULD* be used for the URL of a service or location that "
            "can provide access to this distribution, typically through a Web form, "
            "query or API call.\n`downloadURL` is preferred for direct links to "
            "downloadable resources."
        ),
    )
    accessService: Optional[str] = Field(
        None,
        description=(
            "A data service that gives access to the distribution of the dataset."
        ),
    )
    license: Optional[str] = Field(
        None,
        description=(
            "A legal document under which the distribution is made available."
        ),
    )
    accessRights: Optional[str] = Field(
        None,
        description=(
            "A rights statement that concerns how the distribution is accessed."
        ),
    )
    publisher: Optional[str] = Field(
        None,
        description="The entity responsible for making the resource/item available.",
    )

    @root_validator
    def ensure_unique_url_pairs(cls, values: "Dict[str, Any]") -> "Dict[str, Any]":
        """Ensure either downloadUrl/mediaType or accessUrl/accessService are defined.

        It's fine to define them all, but at least one complete pair MUST be specified.
        """
        if not (
            all(values.get(_) for _ in ["downloadUrl", "mediaType"])
            or all(values.get(_) for _ in ["accessUrl", "accessService"])
        ):
            raise ValueError(
                "Either of the pairs of attributes downloadUrl/mediaType or "
                "accessUrl/accessService MUST be specified."
            )
        return values

"""
Pydantic ResourceConfig Data Model
"""

from typing import Any, Dict, Optional

from pydantic import AnyUrl, BaseModel, Field, root_validator


class ResourceConfig(BaseModel):
    """Resource Configuration for Dataset Distributions"""

    downloadUrl: Optional[AnyUrl] = Field(
        None,
        description=(
            "Definition: The URL of the downloadable file in a given format. E.g. CSV "
            "file or RDF file.\n\nUsage: `downloadURL` *SHOULD* be used for the URL at"
            " which this distribution is available directly, typically through a HTTPS"
            " Get request or SFTP."
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
    accessUrl: Optional[AnyUrl] = Field(
        None,
        description=(
            "A URL of the resource that gives access to a distribution of "
            "the dataset. E.g. landing page, feed, SPARQL endpoint.\n\nUsage: "
            "`accessURL` *SHOULD* be used for the URL of a service or location that "
            "can provide access to this distribution, typically through a Web form, "
            "query or API call.\n`downloadURL` is preferred for direct links to "
            "downloadable resources.\n"
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
    description: Optional[str] = Field(
        None, description="A free-text account of the distribution."
    )
    publisher: Optional[str] = Field(
        None,
        description="The entity responsible for making the resource/item available.",
    )
    configuration: Optional[Dict] = Field(
        {},
        description="Resource-specific configuration options given as key/value-pairs.",
    )

    @root_validator
    def ensure_unique_url_pairs(  # pylint: disable=no-self-use
        cls, values: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Ensure either downloadUrl/mediaType or accessUrl/accessService are
        defined.
        It's fine to define them all, but at least one complete pair MUST be
        specified."""
        if not (
            all(values.get(_) for _ in ["downloadUrl", "mediaType"])
            or all(values.get(_) for _ in ["accessUrl", "accessService"])
        ):
            raise ValueError(
                "Either of the pairs of attributes downloadUrl/mediaType or "
                "accessUrl/accessService MUST be specified."
            )
        return values

"""Pydantic Resource Configuration Data Model."""

from typing import Annotated, List, Optional

from pydantic import Field, model_validator
from pydantic.networks import Url, UrlConstraints

from oteapi.models.genericconfig import GenericConfig
from oteapi.models.secretconfig import SecretConfig

HostlessAnyUrl = Annotated[Url, UrlConstraints(host_required=False)]


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
            " GET request or SFTP.\n\n"
            "Ref: cdat:downloadURL"
        ),
    )
    mediaType: Optional[str] = Field(
        None,
        description=(
            "The media type of the distribution as defined by IANA "
            "[[IANA-MEDIA-TYPES](https://www.w3.org/TR/vocab-dcat-2/#bib-iana-media-types)]"
            ".\n\nUsage: This property *SHOULD* be used when the media"
            " type of the distribution is defined in IANA "
            "[[IANA-MEDIA-TYPES](https://www.w3.org/TR/vocab-dcat-2/#bib-iana-media-types)].\n\n"
            "Ref: dcat:mediaType"
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
            "downloadable resources.\n\n"
            "Ref: dcat:accessURL"
        ),
    )
    accessService: Optional[str] = Field(
        None,
        description=(
            "A data service that gives access to the distribution of the "
            "dataset.\n\n"
            "Usage: SHOULD be used to link to a description of a "
            "dcat:DataService that can provide access to this distribution.\n\n"
            "Ref: dcat:accessService"
        ),
    )
    license: Optional[str] = Field(
        None,
        description=(
            "A legal document under which the distribution is made "
            "available.\n\n"
            "Usage: Information about licenses and rights MAY be provided "
            "for the Resource. See also guidance at [9. License and rights "
            "statements](https://www.w3.org/TR/vocab-dcat-3/#license-rights)."
            "\n\nRef: dcterms:license"
        ),
    )
    accessRights: Optional[str] = Field(
        None,
        description=(
            "Information about who can access the resource or an indication "
            "of its security status.\n\n"
            "Usage: Information about licenses and rights MAY be provided "
            "for the Resource. See also guidance at [9. License and rights "
            "statements](https://www.w3.org/TR/vocab-dcat-3/#license-rights)."
            "\n\nRef:dcterms:accessRights"
        ),
    )
    publisher: Optional[str] = Field(
        None,
        description=(
            "The entity responsible for making the resource/item "
            "available.\n\n"
            "Usage: Resources of type "
            "[foaf:Agent](http://xmlns.com/foaf/0.1/Agent) are recommended as "
            "values for this property.\n\n"
            "Ref: dcterms:publisher"
        ),
    )
    title: Optional[str] = Field(
        None,
        description="A name given to the resource.\n\nRef: dcterms:title",
    )
    #
    # For now `description` is commented out to avoid name conflice
    # `GenericConfig.description`. Consider to rename
    # `GenericConfig.description` to `GenericConfig.modelDescription`.
    #
    # description: Optional[str] = Field(
    #     None,
    #     description=(
    #         "A free-text account of the resource.\n\nRef: dcterms:description"
    #     ),
    # )
    keyword: Optional[List[str]] = Field(
        None,
        description=(
            "A keyword or tag describing the resource.\n\n"
            "Note: Keywords are useful for making the resource easier "
            "searchable.\n\n"
            "Ref: dcat:keyword"
        ),
    )
    conformsTo: Optional[str] = Field(
        None,
        description=(
            "An established standard to which the distribution "
            "conforms.\n\n"
            "Usage: This property SHOULD be used to indicate the model, "
            "schema, ontology, view or profile that this representation "
            "of a dataset conforms to.\n"
            "This is (generally) a complementary concern to the media-type "
            "or format.\n\n"
            "Ref: dcterms:conformsTo"
        ),
    )

    @model_validator(mode="after")
    def ensure_unique_url_pairs(self) -> "ResourceConfig":
        """Ensure either downloadUrl/mediaType or accessUrl/accessService are defined.

        It's fine to define them all, but at least one complete pair MUST be specified.
        """
        if not (
            all(getattr(self, _) for _ in ["downloadUrl", "mediaType"])
            or all(getattr(self, _) for _ in ["accessUrl", "accessService"])
        ):
            raise ValueError(
                "Either of the pairs of attributes downloadUrl/mediaType or "
                "accessUrl/accessService MUST be specified."
            )
        return self

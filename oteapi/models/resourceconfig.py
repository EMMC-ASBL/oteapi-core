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

    resourceType: Optional[str] = Field(
        None, description="Type of registered resource strategy."
    )

    downloadUrl: Optional[HostlessAnyUrl] = Field(
        None,
        description=(
            "The URL of the downloadable file in a given format. E.g. CSV "
            "file or RDF file.\n\n"
            "Usage: `downloadURL` *SHOULD* be used for the URL at which this "
            "distribution is available directly, typically through a HTTPS "
            "GET request or SFTP.\n\n"
            "Range: Resource\n\n"
            "Example: http://dcat.example.org/files/001.csv\n\n"
            "Reference: cdat:downloadURL"
        ),
    )
    mediaType: Optional[str] = Field(
        None,
        description=(
            "The media type of the distribution as defined by IANA "
            "[[IANA-MEDIA-TYPES](https://www.w3.org/TR/vocab-dcat-2/#bib-iana-media-types)]\n\n"
            ".Usage: This property *SHOULD* be used when the media"
            " type of the distribution is defined in IANA "
            "[[IANA-MEDIA-TYPES](https://www.w3.org/TR/vocab-dcat-2/#bib-iana-media-types)].\n\n"
            "Example: text/csv\n\n"
            "Note: In a data catalog should the full IRI be used, i.e. "
            "`http://www.iana.org/assignments/media-types/` should be "
            "pre-pended to the value in this field."
            "Reference: dcat:mediaType"
        ),
    )
    accessUrl: Optional[HostlessAnyUrl] = Field(
        None,
        description=(
            "A URL of the resource that gives access to a distribution of "
            "the dataset. E.g. landing page, feed, SPARQL endpoint.\n\n"
            "Usage: `accessURL` *SHOULD* be used for the URL of a service "
            "or location that can provide access to this distribution, "
            "typically through a Web form, query or API call.\n"
            "`downloadURL` is preferred for direct links to downloadable "
            "resources.\n\n"
            "Example: http://dcat.example.org/dataset-002.html\n\n"
            "Reference: dcat:accessURL"
        ),
    )
    accessService: Optional[str] = Field(
        None,
        description=(
            "A data service that gives access to the distribution of the "
            "dataset.\n\n"
            "Usage: SHOULD be used to link to a description of a "
            "dcat:DataService that can provide access to this distribution.\n\n"
            "Range: Resource\n\n"
            "Example: http://dcat.example.org/table-service-005\n\n"
            "Reference: dcat:accessService"
        ),
    )
    license: Optional[str] = Field(
        None,
        description=(
            "A legal document under which the distribution is made "
            "available.\n\n"
            "Usage: Information about licenses and rights MAY be provided "
            "for the Resource. See also guidance at [9. License and rights "
            "statements](https://www.w3.org/TR/vocab-dcat-3/#license-rights).\n\n"
            "Range: URL to license document (dcterms:LicenseDocument).\n\n"
            "Example: https://creativecommons.org/licenses/by/4.0/\n\n"
            "Reference: dcterms:license"
        ),
    )
    accessRights: Optional[str] = Field(
        None,
        description=(
            "Information about who can access the resource or an indication "
            "of its security status.\n\n"
            "Usage: Information about licenses and rights MAY be provided "
            "for the Resource. See also guidance at [9. License and rights "
            "statements](https://www.w3.org/TR/vocab-dcat-3/#license-rights).\n\n"
            "Range: URL to document describing the license rights "
            "(dcterm:RightsStatement).\n\n"
            "Example: http://publications.europa.eu/resource/authority/access-right/PUBLIC\n\n"
            "Reference: dcterms:accessRights"
        ),
    )
    publisher: Optional[str] = Field(
        None,
        description=(
            "The entity responsible for making the resource/item "
            "available.\n\n"
            "Usage: Resources of type "
            "[foaf:Agent](http://xmlns.com/foaf/0.1/Agent) are recommended "
            "as values for this property.\n\n"
            "Example: http://emmc.eu/\n\n"
            "Reference: dcterms:publisher"
        ),
    )
    creator: Optional[str] = Field(
        None,
        description=(
            "The entity responsible for producing the resource.\n\n"
            "Usage: Resources of type foaf:Agent are recommended as values "
            "for this property.\n\n"
            "Note: For a researcher, this could be the orcid.  For an "
            "instrument, it would be an URL identifying the instrument.\n\n"
            "Example: https://orcid.org/0000-0002-1560-809X\n\n"
            "Reference: dcterms:creator"
        ),
    )
    title: Optional[str] = Field(
        None,
        description="A name given to the resource.\n\nReference: dcterms:title",
    )
    #
    # For now `description` is commented out to avoid name conflice
    # `GenericConfig.description`. Consider to rename
    # `GenericConfig.description` to `GenericConfig.modelDescription`.
    #
    # description: Optional[str] = Field(
    #     None,
    #     description=(
    #         "A free-text account of the resource.\n\n"
    #         "Reference: dcterms:description"
    #     ),
    # )
    keyword: Optional[List[str]] = Field(
        None,
        description=(
            "A keyword or tag describing the resource.\n\n"
            "Note: Keywords are useful for making the resource easier "
            "searchable.\n\n"
            "Reference: dcat:keyword"
        ),
    )
    conformsTo: Optional[str] = Field(
        None,
        description=(
            "An established standard to which the distribution conforms.\n\n"
            "Usage: This property SHOULD be used to indicate the model, "
            "schema, ontology, view or profile that this representation "
            "of a dataset conforms to.\n"
            "This is (generally) a complementary concern to the media-type "
            "or format.\n\n"
            "Range: URL to the standard (dcterms:Standard).\n\n"
            "Example: https://www.w3.org/TR/owl2-overview/\n\n"
            "Reference: dcterms:conformsTo"
        ),
    )
    wasGeneratedBy: Optional[str] = Field(
        None,
        description=(
            "Generation is the completion of production of a new entity by "
            "an activity. This entity did not exist before generation and "
            "becomes available for usage after this generation.\n\n"
            "Range: URL referring generating activity (prov:Activity)\n\n"
            "Example: http://www.ntnu.edu/temgemini/transmission-electron-microscopy\n\n"
            "Reference: prov:wasGeneratedBy"
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
